from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import User, Student, Grade


student_view_bp = Blueprint(
    "student_view",
    __name__,
    url_prefix="/api/student"
)


@student_view_bp.route("/my-grades", methods=["GET"])
@jwt_required()
def my_grades():

    user_id = get_jwt_identity()

    user = db.session.get(
        User,
        int(user_id)
    )

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    # Only students can access this endpoint
    if user.role != "student":
        return jsonify({
            "message": "Student access required"
        }), 403

    # Find the Student record using email
    student = Student.query.filter_by(
        email=user.email
    ).first()

    if not student:
        return jsonify({
            "message": "Student record not found"
        }), 404

    # Get grades belonging to this Student record
    grades = Grade.query.filter_by(
        student_id=student.id
    ).all()

    result = []

    for grade in grades:

        result.append({
            "grade_id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "course_name": (
                grade.course.name
                if grade.course
                else "Unknown"
            ),
            "score": float(grade.score),
            "date": str(grade.date)
        })

    return jsonify({

        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        },

        "grades": result

    }), 200