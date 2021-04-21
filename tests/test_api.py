import pytest
import datetime

from courses_app.models import Course


def test_retrieve_emty_list(client, database):
    response = client.get(
        '/courses'
    )
    assert response.json == []


def test_retrieve_courses_list(client, courses):
    response = client.get(
        '/courses'
    )
    assert len(response.json) == len(courses)
    assert [i['name'] for i in response.json] == [i.name for i in courses]


def test_create_course_200_ok(client, database):
    course_data = {
        "name": "3",
        "starting_date": "2020-05-01",
        "ending_date": "2020-08-12",
        "lectures_count": 3
    }
    response = client.post(
        '/courses',
        json = course_data
    )
    response.json.pop('id')
    assert response.status_code == 200
    assert response.json == course_data


def test_course_name_unique_constrain(client, courses):
    course_data = {
        "name": courses[0].name,
        "starting_date": "2020-5-1",
        "ending_date": "2020-8-12",
        "lectures_count": 3
    }
    response = client.post(
        '/courses',
        json = course_data
    )
    assert response.status_code == 400


def test_course_retrieve_by_id_200_ok(client, courses):
    id = 1
    course = Course.query.get(id)
    response = client.get(
        f'/courses/{id}'
    )
    assert response.status_code == 200
    assert response.json['name'] == course.name


def test_delete_course_by_id_200_ok(client, courses):
    id = 1
    response = client.delete(
        f'/courses/{id}'
    )
    course = Course.query.get(id)
    assert response.status_code == 200
    assert course is None


def test_try_to_delete_not_existed_course(client, courses):
    id = 1245
    response = client.delete(
        f'/courses/{id}'
    )
    assert response.status_code == 400


def test_update_course_attributes(client, courses):
    id = 1
    course_data = {
        "name": "New name",
        "starting_date": "2020-5-1",
        "ending_date": "2020-8-12",
        "lectures_count": 8
    }
    response = client.put(
        f'/courses/{id}',
        json = course_data
    )
    course = Course.query.get(id)
    assert response.status_code == 200
    assert response.json['name'] == "New name"
    assert course.name == "New name"