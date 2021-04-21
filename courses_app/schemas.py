from marshmallow import Schema, fields


class CourseShema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    starting_date = fields.Date()
    ending_date = fields.Date()
    lectures_count = fields.Integer()
