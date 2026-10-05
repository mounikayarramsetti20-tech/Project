from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import pandas as pd
import numpy as np

from models import Grade, Student, Course


analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/api/analytics"
)


@analytics_bp.route("", methods=["GET"])
@jwt_required()
def analytics():

    student_id = request.args.get(
        "student_id",
        type=int
    )

    course_id = request.args.get(
        "course_id",
        type=int
    )

    query = Grade.query

    if student_id:
        query = query.filter_by(
            student_id=student_id
        )

    if course_id:
        query = query.filter_by(
            course_id=course_id
        )

    grades = query.all()

    if not grades:
        return jsonify({
            "message": "No grade data available"
        }), 404

    # Create Pandas DataFrame
    data = []

    for grade in grades:

        student = db_student = Student.query.get(
            grade.student_id
        )

        course = db_course = Course.query.get(
            grade.course_id
        )

        data.append({
            "grade_id": grade.id,
            "student_id": grade.student_id,
            "student_name": (
                student.name
                if student
                else "Unknown"
            ),
            "course_id": grade.course_id,
            "course_name": (
                course.name
                if course
                else "Unknown"
            ),
            "score": float(grade.score)
        })

    df = pd.DataFrame(data)

    scores = df["score"].to_numpy()

    # NumPy statistics
    mean = np.mean(scores)
    median = np.median(scores)
    standard_deviation = np.std(
        scores,
        ddof=0
    )

    # Pandas course averages
    course_average_df = (
        df.groupby(
            ["course_id", "course_name"],
            as_index=False
        )["score"]
        .mean()
    )

    course_average_df = course_average_df.rename(
        columns={
            "score": "average_score"
        }
    )

    course_average = []

    for _, row in course_average_df.iterrows():

        course_average.append({
            "course_id": int(row["course_id"]),
            "course_name": row["course_name"],
            "average_score": round(
                float(row["average_score"]),
                2
            )
        })

    # Ranking using Pandas
    ranking_df = df.sort_values(
        by="score",
        ascending=False
    ).reset_index(drop=True)

    ranking_result = []

    for position, row in ranking_df.iterrows():

        ranking_result.append({
            "rank": position + 1,
            "student_id": int(
                row["student_id"]
            ),
            "student_name": row["student_name"],
            "course_id": int(
                row["course_id"]
            ),
            "course_name": row["course_name"],
            "score": float(row["score"])
        })

    return jsonify({
        "filters": {
            "student_id": student_id,
            "course_id": course_id
        },
        "statistics": {
            "mean": round(
                float(mean),
                2
            ),
            "median": round(
                float(median),
                2
            ),
            "standard_deviation": round(
                float(standard_deviation),
                2
            )
        },
        "course_average": course_average,
        "ranking": ranking_result
    }), 200