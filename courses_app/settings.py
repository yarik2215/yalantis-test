import os


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite"

    HOST = "localhost"
    PORT = "5000"

    SECRET_KEY = "replace_it"

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
