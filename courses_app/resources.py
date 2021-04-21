import datetime
from flask import request
from flask_restplus import Resource, Api, fields
from marshmallow.fields import Date

from courses_app.models import Course, db
from courses_app.schemas import CourseShema

from webargs import fields as args_fields
from webargs.flaskparser import use_kwargs

api = Api(doc='/docs')

course_fields = api.model('Course', {
    'name': fields.String,
    "starting_date": fields.Date,
    "ending_date": fields.Date,
    'lectures_count': fields.Integer,
})


@api.route('/courses')
@api.doc()
class CoursesList(Resource):

    @api.doc(params={'q': 'name or part of it', 'date': 'date'})
    @use_kwargs({'q': args_fields.String(), 'date': args_fields.Date()}, location='query')
    def get(self, q: str = None, date: datetime.date = None):
        courses_query = Course.query
        if q:
            courses_query = courses_query.filter(Course.name.contains(q)) 
        if date:
            courses_query = courses_query.filter(Course.starting_date <= date, Course.ending_date >= date)
        courses = courses_query.all()
        return CourseShema(many=True, only=['id', 'name']).dump(courses)

    @api.expect(course_fields)
    def post(self):
        course_data = CourseShema().load(
            request.get_json()
        )
        course = Course(**course_data)
        db.session.add(course)
        db.session.commit()
        return CourseShema().dump(course)


@api.route('/courses/<int:id>')
@api.doc(params={'id': 'Course id'})
class CoursesDetailed(Resource):
    def _get_object(self, id: int) -> Course:
        return Course.query.get(id)

    def get(self, id: int):
        request
        course = self._get_object(id)
        return CourseShema().dump(course)
    
    @api.expect(course_fields)
    def put(self, id: int):
        course_data = CourseShema(partial=True).load(
            request.get_json()
        )
        course = self._get_object(id)
        return CourseShema().dumps(course)
    
    def delete(self, id: int):
        Course.query.delete(id)