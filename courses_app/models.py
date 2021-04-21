
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    starting_date = db.Column(db.Date())
    ending_date = db.Column(db.Date())
    lectures_count = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
