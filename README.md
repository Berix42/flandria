# Flandria
![](/webapp/static/assets/logo.png?raw=True)


Starting 01.01.2022, I stopped working on Flandria and took the website down.

If you're considering hosting the website yourself, please remove my personal about page, legal notice and donation links before publishing. The site should not include any information about me anymore.
Please be wary, that I did not update any security over the years, so it is probably not safe to use as it is.
There's also no documentation on how to do things and I won't provide any support or help.

Please also honor the License applied to the project.

Thanks for all the support over the years.

Install all requirements.
```commandline
pip install -r requirements.txt
```

## Run flask-server ####
```commandline
FLASK_ENV=development FLASK_APP=app.py flask run --host=0.0.0.0 --port 5000
```

## Initialize database
Run the following commands with virtual environment.
```commandline
flask db upgrade
```

## Populate database with data
Download data from Florensia:
```commandline
flask updater download
```
Update database:
```commandline
flask updater database
```
Update icons:
```commandline
flask updater icons
```

## Update player ranking
```commandline
flask tasks update-ranking
```

## Installation ##
This section explains how to install and run the application-stack. If you want to start with _developing_ see section
[run flask-server](#run-flask-server) instead.</br>
Building the docker image on your local machine requires that [docker](https://docs.docker.com/get-docker/) is installed
and its daemon is running. Check out [rootless mode](https://docs.docker.com/engine/security/rootless/#install)
for installing / running docker without root privileges. Additionally,
[docker-compose](https://docs.docker.com/compose/install/) is needed to run the containers together. The following
commands should not return an error after installing and running docker:
```commandline
docker info
docker --version
docker-compose --version
```
After a successful installation, start by cloning the repository:
```commandline
git clone https://github.com/lauderandtaiga/flandria.git
cd flandria
```
First the docker-image is build locally. This will take some time if the image was never built before on this machine,
so go get a coffee :) Building again will make use of caching and therefore should be much faster than building for the
first time.
Change to the directory that contains the "docker-compose"-File and run the
build-command:
```commandline
cd run_stack
docker-compose build
```
If the application is run in a development environment the server can be reached under "localhost" as defined in the
nginx configuration and no site-name or ssl-certificate is needed.</br>
If deploying to a production environment, **ssl-certificates** and the site-name is needed to properly configure nginx.
Therefore, you should place your ssl-certificates in the ssl-cert-folder:
```commandline
cd nginx/ssl_certs
cp /etc/ssl/certs/my_ssl_cert.crt ssl.cert
cp /etc/ssl/certs/my_ssl_key.key ssl.key
```
And specify your site-name on startup. Run the application-stack in production (will require ssl-certificate):
```commandline
APP_ENV=prod SITE_NAME=flandria.info docker-compose up -d
```
Or for development on "localhost":
```commandline
APP_ENV=dev docker-compose up -d
```
Hint: Leaving the "APP_ENV"-variable unset will result in production-behaviour. This is intended to prevent forgetting
to supply the correct variable in production and thus bypassing the ssl-certification.</br>
Open a browser and check if you can reach the server. Additional firewall-settings might be needed to open up ports
80 (http) and 443 (https) to the internet.

### Update installation ###
Stop the application-stack:
```commandline
cd flandria/run_stack
docker-compose down
```
Get new version of master-branch from git-repository:
```commandline
git checkout master
git pull origin master
```
Build docker-image:
```commandline
docker-compose build
```
Run the stack again:
```commandline
APP_ENV=prod SITE_NAME=flandria.info docker-compose up -d
```