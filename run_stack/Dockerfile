FROM node:bullseye AS build

# Disable interactive mode = disable dialogs from apt while installing (e.g. to install npm)
ENV DEBIAN_FRONTEND noninteractive
# Install python and add aliases for python-command, so they are available to the following scripts (especially "after_build.py")
RUN apt-get -y update  \
    && apt-get -y install python3.9 python3-pip \
    && ln -s $(which python3.9) /usr/bin/python && ln -s $(which python3.9) /usr/bin/py

# Add new user for flandria-server
RUN useradd -ms /bin/bash flandria_user && chown flandria_user /home/flandria_user

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

# Multi-stage build (copy needed files from previouse stage to decrease number of layers and size of resulting image)
FROM python:3.9-slim-bullseye

# Add new user for flandria-server
RUN useradd -ms /bin/bash flandria_user && chown flandria_user /home/flandria_user
WORKDIR /home/flandria_user/flandria

# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy only needed files from build-stage or local repository
COPY --from=build --chown=flandria_user /home/flandria_user/flandria/webapp webapp
COPY --chown=flandria_user app.py run_stack/wsgi.py ./
ADD --chown=flandria_user database_updater database_updater
ADD --chown=flandria_user migrations migrations

# Start webserver
# Replace Flask internal server with Gunicorn (application server) for productional usage
# See: https://www.toptal.com/flask/flask-production-recipes
USER flandria_user
EXPOSE 5000
CMD gunicorn --workers 8 --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info