from flask import Blueprint
from flask.app import Flask
from flask_restful import Api, Resource
from courses_app import resources


def register_routes(_app: Flask):
    """Registers api resources/routes with Flask app

    Args:
        _app (object): Flask app object

    """

    api_blueprint = Blueprint("api", __name__)
    api = Api(api_blueprint, catch_all_404s=False)

    api.add_resource(
        resources.CoursesList, "/courses")
    api.add_resource(
        resources.CoursesDetailed, "/courses/<int:id>")

    _app.register_blueprint(api_blueprint, url_prefix="/api")