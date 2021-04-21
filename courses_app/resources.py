import datetime
from flask import request, abort
from flask_restplus import Resource, Api, fields
from webargs import fields as args_fields
from webargs.flaskparser import use_kwargs
from sqlalchemy import exc

from courses_app.models import Course, db
from courses_app.schemas import CourseShema


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
        try:
            db.session.add(course)
            db.session.commit()
        except exc.IntegrityError as e:
            abort(400, description=f"Course with name {course.name} already exist")
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
        for key, value in course_data.items():
            setattr(course, key, value)
        db.session.commit()
        return CourseShema().dump(course)
    
    def delete(self, id: int):
        if Course.query.filter_by(id=id).delete() == 0:
            abort(400, f'No course with id {id}')
        db.session.commit()