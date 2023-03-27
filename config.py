import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SEC_KEY") or "tigerFocus098098"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI') or \
        "postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com/tigerfocus_4gqq"

config = {
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}