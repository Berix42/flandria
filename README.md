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