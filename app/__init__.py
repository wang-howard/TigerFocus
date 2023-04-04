"""
Initializes TigerFocus app, db, and cas_client to be used by various
files within app/. The single fuction create_app() creates the Flask
app, initializes the SQLAlchemy object and returns the app. db and
cas_client global variables are imported by other files.
"""

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.cas import CASClient

from config import Config

db = SQLAlchemy()

cas_client = CASClient(version=3, service_url=os.getenv("SERVICE_URL"),
                       server_url="https://fed.princeton.edu/cas/")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Flask SQLAlchemy extension
    db.init_app(app)

    # register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
