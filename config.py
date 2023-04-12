"""
Configuration file for Flask app. Sets necessary environment variables
for Flask and SQLAlchemy.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SEC_KEY") or "tigerFocus098098"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
        "postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com/tigerfocus_4gqq"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # connection pooling configurations
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = 1800
