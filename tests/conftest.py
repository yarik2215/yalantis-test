import os
import tempfile
import datetime

import pytest

from courses_app import create_app
from courses_app import settings
from courses_app.models import db, Course


@pytest.fixture(scope="module")
def app():
    db_fd, db_path = tempfile.mkstemp()

    class TestingConfig(settings.DevelopmentConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"

    app = create_app(TestingConfig)
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def database(app):
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def create_course(
    name: str, starting_date: datetime.date = datetime.date.today(), duration_days: int = 10, lectures_count: int = 10 
):
    return Course(
        name = name,
        starting_date = starting_date,
        ending_date = starting_date + datetime.timedelta(days=duration_days),
        lectures_count = lectures_count
    )

@pytest.fixture
def courses(database):
    courses = [
        create_course(f'Course{i}', duration_days=i)
        for i in range(1, 5)
    ]
    database.session.add_all(courses)
    return courses