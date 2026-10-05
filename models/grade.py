from extensions import db
from datetime import datetime


class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )
    score = db.Column(db.Float, nullable=False)
    date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    student = db.relationship("Student", backref="grades")
    course = db.relationship("Course", backref="grades")