from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Student, User


students_bp = Blueprint(
    "students",
    __name__,
    url_prefix="/api/students"
)


def is_admin():

    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return False

    return user.role == "admin"


@students_bp.route("", methods=["GET"])
@jwt_required()
def get_students():

    students = Student.query.all()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email
        })

    return jsonify(result), 200


@students_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_student(id):

    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email
    }), 200


@students_bp.route("", methods=["POST"])
@jwt_required()
def create_student():

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
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "message": "Name and email are required"
        }), 400

    existing_student = Student.query.filter_by(
        email=email
    ).first()

    if existing_student:
        return jsonify({
            "message": "Student email already exists"
        }), 409

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 201


@students_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_student(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    student.name = data.get(
        "name",
        student.name
    )

    student.email = data.get(
        "email",
        student.email
    )

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


@students_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch_student(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "JSON data is required"
        }), 400

    if "name" in data:
        student.name = data["name"]

    if "email" in data:
        student.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "Student partially updated successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email
        }
    }), 200


@students_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_student(id):

    if not is_admin():
        return jsonify({
            "message": "Admin access required"
        }), 403

    student = db.session.get(Student, id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    db.session.delete(student)

    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200