import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from cas import CASClient

from config import Config

db = SQLAlchemy()

cas_client = CASClient(version=3, service_url=os.getenv("SERVICE_URL"),
                       server_url="https://fed.princeton.edu/cas/")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Flask SQLAlchemy extension
    db.init_app(app)

    # register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    # attach routes and custom error pages here

    return app
