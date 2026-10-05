from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Course, User


courses_bp = Blueprint(
    "courses",
    __name__,
    url_prefix="/api/courses"
)


def is_admin():

    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return False

    return user.role == "admin"


@courses_bp.route("", methods=["GET"])
@jwt_required()
def get_courses():

    courses = Course.query.all()

    result = []

    for course in courses:

        result.append({
            "id": course.id,
            "name": course.name,
            "code": course.code
        })

    return jsonify(result), 200


@courses_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_course(id):

    course = db.session.get(Course, id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    return jsonify({
        "id": course.id,
        "name": course.name,
        "code": course.code
    }), 200


@courses_bp.route("", methods=["POST"])
@jwt_required()
def create_course():

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    name = data.get("name")
    code = data.get("code")

    if not name or not code:
        return jsonify({
            "message": "Course name and code are required"
        }), 400

    existing_course = Course.query.filter_by(
        code=code
    ).first()

    if existing_course:
        return jsonify({
            "message": "Course code already exists"
        }), 409

    course = Course(
        name=name,
        code=code
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        "message": "Course created successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 201


@courses_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_course(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    course = db.session.get(Course, id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    course.name = data.get(
        "name",
        course.name
    )

    course.code = data.get(
        "code",
        course.code
    )

    db.session.commit()

    return jsonify({
        "message": "Course updated successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


@courses_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_course(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    course = db.session.get(Course, id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    if "name" in data:
        course.name = data["name"]

    if "code" in data:
        course.code = data["code"]

    db.session.commit()

    return jsonify({
        "message": "Course partially updated successfully",
        "course": {
            "id": course.id,
            "name": course.name,
            "code": course.code
        }
    }), 200


@courses_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_course(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    course = db.session.get(Course, id)

    if not course:
        return jsonify({
            "message": "Course not found"
        }), 404

    db.session.delete(course)

    db.session.commit()

    return jsonify({
        "message": "Course deleted successfully"
    }), 200