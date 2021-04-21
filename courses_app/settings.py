import os


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/db.sqlite"

    HOST = "localhost"
    PORT = "5000"

    SECRET_KEY = "replace_it"

    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DevelopmentConfig.BASE_DIR}/test_db.sqlite"