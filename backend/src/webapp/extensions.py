from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_caching import Cache

AUTH_KEY = 'apikey'
authorizations = {
    AUTH_KEY: {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}

db = SQLAlchemy()
migrate = Migrate()
api_ = Api(version="1.0", title="Flandria API", prefix="/api", doc="/api", authorizations=authorizations)
jwt = JWTManager()
cache = Cache()
