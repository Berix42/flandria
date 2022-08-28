from database_updater.cli import drops_cli, updater_cli
from flask import Flask

from webapp.api.auth import LoginView, RegisterView
from webapp.api.database import DetailedTableView, MapView, Search, TableView
from webapp.api.planner import PlannerView, PlannerBuildView, PlannerStarView
from webapp.api.ranking import (GuildDetailedView, GuildOverviewView,
                                RankingStatisticsView, PlayerDetailedView,
                                PlayerOverviewView)
from webapp.config import DevelopmentConfig, ProductionConfig, TestingConfig
from webapp.extensions import api_, cache, db, jwt, migrate
from webapp.tasks import tasks_cli
from webapp.utils import gzip_response, set_cors_header  # noqa: F401
from webapp.loaders import user_lookup_loader

import os


def create_app() -> Flask:
    """Creates and configures a flask application object.

    Returns:
        Flask: The application object.
    """
    app = Flask(__name__)

    # Strings that determine the environment (dev/prod/test) of the current instance when set in env-var "APP_ENV"
    DEV_STR = "dev"
    PROD_STR = "prod"
    TEST_STR = "test"
    app_env_cases = {
        DEV_STR: DevelopmentConfig,
        PROD_STR: ProductionConfig,
        TEST_STR: TestingConfig
    }

    # Enable api-validation via swagger-definition application-wide for every endpoint
    app.config['RESTX_VALIDATE'] = True

    # Load config corresponding to current environment
    APP_ENV = os.environ.get("APP_ENV", DEV_STR)
    app.config.from_object(app_env_cases[APP_ENV] if APP_ENV in app_env_cases else DevelopmentConfig)

    # Extensions
    register_extensions(app)

    # Register api endpoints
    register_api_endpoints()

    # Commands
    register_commands(app)

    # Register functions for extensions
    jwt.user_lookup_loader(user_lookup_loader)

    # Register teardown functions
    # app.after_request(gzip_response)
    if APP_ENV == DEV_STR:
        app.after_request(set_cors_header)

    # Clear cache on startup
    with app.app_context():
        cache.clear()

    return app


def register_extensions(app: Flask) -> None:
    """Registers flask extensions to the application object.

    Args:
        app (Flask): The flask application object.
    """
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    api_.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)


def register_commands(app: Flask) -> None:
    """Registers custom commands to the flask db utilities.

    Args:
        app (Flask): The flask application object.
    """
    app.cli.add_command(updater_cli)
    app.cli.add_command(drops_cli)
    app.cli.add_command(tasks_cli)


def register_api_endpoints() -> None:

    # Database API
    database_ns = api_.namespace("database")
    database_ns.add_resource(TableView, "/<table>")
    database_ns.add_resource(DetailedTableView, "/<table>/<code>")
    database_ns.add_resource(Search, "/search")
    database_ns.add_resource(MapView, "/map/<code>")

    # Auth API
    auth_ns = api_.namespace("auth")
    auth_ns.add_resource(RegisterView, "/register")
    auth_ns.add_resource(LoginView, "/login")

    # Planner API
    planner_ns = api_.namespace("planner")
    planner_ns.add_resource(PlannerView, "/<classname>")
    planner_ns.add_resource(PlannerBuildView, "/builds/<string:classname>", methods=['GET'])
    planner_ns.add_resource(PlannerBuildView, "/builds", methods=['POST'])
    planner_ns.add_resource(PlannerBuildView, "/builds/<int:id>", methods=['DELETE'])
    planner_ns.add_resource(PlannerStarView, "/builds/<int:build_id>/star")

    # Ranking API
    ranking_ns = api_.namespace("ranking")
    ranking_ns.add_resource(RankingStatisticsView, "/statistics")
    ranking_ns.add_resource(GuildOverviewView, "/guilds")
    ranking_ns.add_resource(GuildDetailedView, "/guilds/<path:name>")
    ranking_ns.add_resource(PlayerOverviewView, "/players")
    ranking_ns.add_resource(PlayerDetailedView, "/players/<server>/<name>")
