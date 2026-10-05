from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Grade, Student, Course, User


grades_bp = Blueprint(
    "grades",
    __name__,
    url_prefix="/api/grades"
)


def is_admin():

    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return False

    return user.role == "admin"


@grades_bp.route("", methods=["GET"])
@jwt_required()
def get_grades():

    grades = Grade.query.all()

    result = []

    for grade in grades:

        result.append({
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date
        })

    return jsonify(result), 200


@grades_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_grade(id):

    grade = db.session.get(Grade, id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    return jsonify({
        "id": grade.id,
        "student_id": grade.student_id,
        "course_id": grade.course_id,
        "score": grade.score,
        "date": grade.date
    }), 200


@grades_bp.route("", methods=["POST"])
@jwt_required()
def create_grade():

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    student_id = data.get("student_id")
    course_id = data.get("course_id")
    score = data.get("score")

    if student_id is None or course_id is None or score is None:
        return jsonify({
            "message": "student_id, course_id and score are required"
        }), 400

    student = db.session.get(Student, student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    course = db.session.get(Course, course_id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    try:
        score = float(score)

    except (TypeError, ValueError):

        return jsonify({
            "message": "Score must be a number"
        }), 400

    if score < 0 or score > 100:

        return jsonify({
            "message": "Score must be between 0 and 100"
        }), 400

    grade = Grade(
        student_id=student_id,
        course_id=course_id,
        score=score
    )

    db.session.add(grade)

    db.session.commit()

    return jsonify({
        "message": "Grade created successfully",
        "grade": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date
        }
    }), 201


@grades_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_grade(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    grade = db.session.get(Grade, id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    if "score" in data:

        try:
            score = float(data.get("score"))

        except (TypeError, ValueError):

            return jsonify({
                "message": "Score must be a number"
            }), 400

        if score < 0 or score > 100:

            return jsonify({
                "message": "Score must be between 0 and 100"
            }), 400

        grade.score = score

    db.session.commit()

    return jsonify({
        "message": "Grade updated successfully",
        "grade": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date
        }
    }), 200


@grades_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_grade(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    grade = db.session.get(Grade, id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    if "score" in data:

        try:
            score = float(data.get("score"))

        except (TypeError, ValueError):

            return jsonify({
                "message": "Score must be a number"
            }), 400

        if score < 0 or score > 100:

            return jsonify({
                "message": "Score must be between 0 and 100"
            }), 400

        grade.score = score

    db.session.commit()

    return jsonify({
        "message": "Grade partially updated successfully",
        "grade": {
            "id": grade.id,
            "student_id": grade.student_id,
            "course_id": grade.course_id,
            "score": grade.score,
            "date": grade.date
        }
    }), 200


@grades_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_grade(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    grade = db.session.get(Grade, id)

    if not grade:
        return jsonify({
            "message": "Grade not found"
        }), 404

    db.session.delete(grade)

    db.session.commit()

    return jsonify({
        "message": "Grade deleted successfully"
    }), 200