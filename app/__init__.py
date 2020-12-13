from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    migrate = Migrate(app, db)

    from app import models

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
