# Flandria
![](/webapp/static/assets/logo.png?raw=True)


Starting 01.01.2022, I stopped working on Flandria and took the website down.

If you're considering hosting the website yourself, please remove my personal about page, legal notice and donation links before publishing. The site should not include any information about me anymore.
Please be wary, that I did not update any security over the years, so it is probably not safe to use as it is.
There's also no documentation on how to do things and I won't provide any support or help.

Please also honor the License applied to the project.

Thanks for all the support over the years.

## Project structure
![](C:\Projekte\Flandria\flandria\docs\flandria_stack.jpg)

Folder            | Purpose
------------------|----------
database_updater  | Populate database with data from online resource
docs              | Keep track of documentation files
frontend          | Frontend files (assets / javascript etc.)
migrations        | Adjusting database scheme
run_stack         | Deployment files (docker + config-files)
webapp            | Backend files (application logic)

Live Swagger-doc of endpoints can be found at _/api_.

Contribute to the project
--------------------------------
Clone repository:
```
git clone https://github.com/lauderandtaiga/flandria.git
```
Install requirements for backend (python installation required, might want to look at _virtual environments_ beforehand):
```commandline
cd flandria
pip install -r requirements.txt
```
Install requirements for frontend (nodejs installation required):
```commandline
cd frontend
npm install
```
Run backend for development:
```commandline
cd flandria
FLASK_ENV=development FLASK_APP=app.py flask run --host=0.0.0.0 --port 5000
```
Run frontend with hot-reload feature:
```commandline
cd frontend
PORT=80 npm run start
```
With running backend and running frontend check [localhost](http://localhost), you should now see the website.

Initialize database
--------------------------------
This will create the database and the tables.
```commandline
flask db upgrade
```

Populate database with data
--------------------------------
Download data from Florensia:
```commandline
flask updater download
```
Update database:
```commandline
flask updater database
```

Additional commands
--------------------------------
Update player ranking. This includes guilds.
```commandline
flask tasks update-ranking
```
Update icons:
```commandline
flask updater icons
```

## Installation ##
This section explains how to install and run the application-stack. If you want to start with _developing_ see section
[run flask-server](#run-flask-server) instead.</br>
Running the docker image on your local machine requires that [docker](https://docs.docker.com/get-docker/) is installed
and its daemon is running. Check out [rootless mode](https://docs.docker.com/engine/security/rootless/#install)
for installing / running docker without root privileges. The following
commands should not return an error after installing and running docker:
```commandline
docker info
docker --version
docker compose version
```
After a successful installation, start by cloning the repository:
```commandline
git clone https://github.com/lauderandtaiga/flandria.git
cd flandria
```
If the application is run in a development environment the server can be reached under [localhost](http://localhost/)
and no site-name or ssl-certificate is needed.</br>
If deploying to a production environment, **ssl-certificate** and the site-name is needed to properly configure the
reverse proxy.
Therefore, you should place your ssl-certificate in the ssl-cert-folder:
```commandline
cd run_stack/ssl_certs
cp /etc/ssl/certs/my_ssl_cert.crt flandria.wiki.cert
cp /etc/ssl/certs/my_ssl_key.key flandria.wiki.key
```
The certificate and key should be named after the virtual host with a .crt and .key extension. For example, if your
site name is "flandria.wiki" you should have a flandria.wiki.crt and flandria.wiki.key file in the certs directory. Look
[here](https://github.com/nginx-proxy/nginx-proxy) for more infos.</br>
Specify your site-name on startup and run the application-stack in production:
```commandline
APP_ENV=prod SITE_NAME=flandria.wiki docker compose up -d
```
Or for development on "localhost":
```commandline
APP_ENV=dev docker compose up -d
```
Hint: Leaving the "APP_ENV"-variable unset will result in production-behaviour. This is intended to prevent forgetting
to supply the correct variable in production.</br>
Open a browser and check if you can reach the server. Additional firewall-settings might be needed to open up ports
80 (http) and 443 (https) to the internet.

### Update installation ###
Gets new images from [DockerHub](https://hub.docker.com/r/florensiacommunity/flandria), restarts only containers with
changed image and cleans up unneeded image-space afterwards:
```commandline
docker compose pull
APP_ENV=prod SITE_NAME=flandria.wiki docker compose up -d
docker image prune
```
As an alternative you can install [webhook](https://github.com/adnanh/webhook) on your machine for an automatic
deployment triggered directly from GitHub.
