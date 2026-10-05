from flask import Blueprint, Response, request, jsonify
from flask_jwt_extended import jwt_required
from models import Grade, Student, Course
from extensions import db

import csv
import io

from openpyxl import Workbook


reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/api/reports"
)


@reports_bp.route("/csv", methods=["GET"])
@jwt_required()
def export_csv():

    grades = Grade.query.all()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Grade ID",
        "Student ID",
        "Course ID",
        "Score",
        "Date"
    ])

    for grade in grades:
        writer.writerow([
            grade.id,
            grade.student_id,
            grade.course_id,
            grade.score,
            grade.date
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=student_grades.csv"
    )

    return response


@reports_bp.route("/excel", methods=["GET"])
@jwt_required()
def export_excel():

    grades = Grade.query.all()

    workbook = Workbook()
    sheet = workbook.active

    sheet.title = "Student Grades"

    sheet.append([
        "Grade ID",
        "Student ID",
        "Course ID",
        "Score",
        "Date"
    ])

    for grade in grades:
        sheet.append([
            grade.id,
            grade.student_id,
            grade.course_id,
            grade.score,
            str(grade.date)
        ])

    output = io.BytesIO()

    workbook.save(output)

    output.seek(0)

    response = Response(
        output.getvalue(),
        mimetype=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=student_grades.xlsx"
    )

    return response


@reports_bp.route("/upload-csv", methods=["POST"])
@jwt_required()
def upload_csv():

    file = request.files.get("file")

    if not file:
        return jsonify({
            "message": "CSV file is required"
        }), 400

    if not file.filename.endswith(".csv"):
        return jsonify({
            "message": "Only CSV files are allowed"
        }), 400

    try:
        content = file.read().decode("utf-8")

        csv_file = io.StringIO(content)

        reader = csv.DictReader(csv_file)

        imported = 0

        for row in reader:

            student_id = int(row["student_id"])
            course_id = int(row["course_id"])
            score = float(row["score"])

            if score < 0 or score > 100:
                continue

            student = db.session.get(Student, student_id)
            course = db.session.get(Course, course_id)

            if not student or not course:
                continue

            grade = Grade(
                student_id=student_id,
                course_id=course_id,
                score=score
            )

            db.session.add(grade)

            imported += 1

        db.session.commit()

        return jsonify({
            "message": "CSV uploaded successfully",
            "records_imported": imported
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "message": "Invalid CSV file",
            "error": str(e)
        }), 400