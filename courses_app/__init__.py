from flask import Flask

from courses_app import settings
from courses_app.resources import api


def create_app(config_obj=None):
    app = Flask(__name__, static_folder=None)

    if not config_obj:
        app.logger.warning(
            "No config specified; defaulting to development"
        )
        config_obj = settings.DevelopmentConfig

    app.config.from_object(config_obj)

    from courses_app.models import db, migrate

    db.init_app(app)
    db.app = app

    migrate.init_app(app, db)

    api.init_app(app)

    return app
