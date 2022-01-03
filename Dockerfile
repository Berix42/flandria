FROM ubuntu:21.10 AS build

# Install required packages
# Disable interactive mode = disable dialogs from apt while installing (e.g. to install npm)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install nodejs npm python3.9 python3-pip
# Add aliases for python-command, so they are available to the following scripts (especially "after_build.py")
RUN ln -s $(which python3.9) /usr/bin/python && ln -s $(which python3.9) /usr/bin/py

# Add new user for flandria-server
RUN useradd -ms /bin/bash flandria_user && chown flandria_user /home/flandria_user

# Install python-packages
WORKDIR /home/flandria_user/flandria
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install frontend dependencies
WORKDIR /home/flandria_user/flandria/flandria-frontend
ADD --chown=flandria_user flandria-frontend/package.json .
ADD --chown=flandria_user flandria-frontend/package-lock.json .
RUN npm install
# Build frontend
COPY --chown=flandria_user after_build.py ..
ADD --chown=flandria_user webapp ../webapp
ADD --chown=flandria_user flandria-frontend .
# The build-directive in "flandria-frontend/package.json" copies the files after building to the webapp-dirs
RUN npm run build

# Prepare icons to be copied to next stage ("after_build"-script deletes whole assets-folder)
WORKDIR /home/flandria_user/flandria/webapp/static/assets
ADD --chown=flandria_user webapp/static/assets/item_icons item_icons
ADD --chown=flandria_user webapp/static/assets/monster_icons monster_icons
ADD --chown=flandria_user webapp/static/assets/npc_icons npc_icons
ADD --chown=flandria_user webapp/static/assets/skill_icons skill_icons

# Multi-stage build (copy needed files from previouse stage to decrease number of layers and size of resulting image)
# Use alpine-image as base for smaller resulting image
FROM python:3.9.5-alpine

# Add new user for flandria-server
RUN adduser -S flandria_user && chown flandria_user /home/flandria_user
WORKDIR /home/flandria_user/flandria

# Install requirements
# Alpine image does not contain some packages that needed for some of the requirements (e.g. Pillow) -> install them
COPY requirements.txt .
RUN apk add build-base jpeg-dev zlib-dev
RUN pip install -r requirements.txt

# Copy only needed files from build-stage or local repository
COPY --from=build --chown=flandria_user /home/flandria_user/flandria/webapp webapp
COPY --chown=flandria_user app.py .
ADD --chown=flandria_user database_updater database_updater
ADD --chown=flandria_user migrations migrations

# Start webserver
# TODO: Replace Flask internal server with application server for productional usage
USER flandria_user
ENV FLASK_ENV=development
ENV FLASK_APP=app.py
EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000"]