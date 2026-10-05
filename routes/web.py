from flask import Blueprint, render_template, request, redirect, url_for

from models import Student, Course, Grade
from extensions import db


web_bp = Blueprint(
    "web",
    __name__
)


# ================================
# DASHBOARD
# ================================

@web_bp.route("/dashboard")
def dashboard():

    students = Student.query.all()
    courses = Course.query.all()
    grades = Grade.query.all()

    scores = [float(grade.score) for grade in grades]

    if scores:

        mean = sum(scores) / len(scores)

        sorted_scores = sorted(scores)
        n = len(sorted_scores)

        if n % 2 == 1:
            median = sorted_scores[n // 2]
        else:
            median = (
                sorted_scores[n // 2 - 1]
                + sorted_scores[n // 2]
            ) / 2

        variance = sum(
            (score - mean) ** 2
            for score in scores
        ) / len(scores)

        standard_deviation = variance ** 0.5

    else:

        mean = 0
        median = 0
        standard_deviation = 0

    ranking = sorted(
        grades,
        key=lambda grade: grade.score,
        reverse=True
    )

    return render_template(
        "dashboard.html",
        students=students,
        courses=courses,
        grades=grades,
        mean=round(mean, 2),
        median=round(median, 2),
        standard_deviation=round(
            standard_deviation,
            2
        ),
        ranking=ranking
    )


# ================================
# LOGIN
# ================================

@web_bp.route("/login")
def login_page():

    return render_template("login.html")


# ================================
# STUDENTS
# ================================

@web_bp.route("/students")
def students():

    student_list = Student.query.all()

    return render_template(
        "students/list.html",
        students=student_list
    )


@web_bp.route("/students/new")
def new_student():

    return render_template(
        "students/form.html"
    )


@web_bp.route("/students", methods=["POST"])
def create_student():

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Name and email are required", 400

    existing_student = Student.query.filter_by(
        email=email
    ).first()

    if existing_student:
        return "Student email already exists", 409

    student = Student(
        name=name,
        email=email
    )

    db.session.add(student)
    db.session.commit()

    return redirect(
        url_for("web.students")
    )


@web_bp.route("/students/<int:id>")
def student_detail(id):

    student = db.session.get(
        Student,
        id
    )

    if not student:
        return "Student not found", 404

    return render_template(
        "students/detail.html",
        student=student
    )


@web_bp.route("/students/<int:id>/edit")
def edit_student(id):

    student = db.session.get(
        Student,
        id
    )

    if not student:
        return "Student not found", 404

    return render_template(
        "students/form.html",
        student=student
    )


@web_bp.route(
    "/students/<int:id>",
    methods=["POST"]
)
def modify_student(id):

    student = db.session.get(
        Student,
        id
    )

    if not student:
        return "Student not found", 404

    method = request.form.get(
        "_method",
        ""
    ).upper()

    if method == "DELETE":

        if student.grades:

            return (
                "Cannot delete this student because "
                "grades are assigned to the student.",
                400
            )

        db.session.delete(student)
        db.session.commit()

        return redirect(
            url_for("web.students")
        )

    if method in ["PUT", "PATCH"]:

        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return "Name and email are required", 400

        existing_student = Student.query.filter(
            Student.email == email,
            Student.id != id
        ).first()

        if existing_student:
            return "Student email already exists", 409

        student.name = name
        student.email = email

        db.session.commit()

        return redirect(
            url_for(
                "web.student_detail",
                id=id
            )
        )

    return "Invalid method", 400


# ================================
# COURSES
# ================================

@web_bp.route("/courses")
def courses():

    course_list = Course.query.all()

    return render_template(
        "courses/list.html",
        courses=course_list
    )


@web_bp.route("/courses/new")
def new_course():

    return render_template(
        "courses/form.html"
    )


@web_bp.route("/courses", methods=["POST"])
def create_course():

    name = request.form.get("name")
    code = request.form.get("code")

    if not name or not code:
        return "Course name and code are required", 400

    existing_course = Course.query.filter_by(
        code=code
    ).first()

    if existing_course:
        return "Course code already exists", 409

    course = Course(
        name=name,
        code=code
    )

    db.session.add(course)
    db.session.commit()

    return redirect(
        url_for("web.courses")
    )


@web_bp.route("/courses/<int:id>/edit")
def edit_course(id):

    course = db.session.get(
        Course,
        id
    )

    if not course:
        return "Course not found", 404

    return render_template(
        "courses/form.html",
        course=course
    )


@web_bp.route(
    "/courses/<int:id>",
    methods=["POST"]
)
def modify_course(id):

    course = db.session.get(
        Course,
        id
    )

    if not course:
        return "Course not found", 404

    method = request.form.get(
        "_method",
        ""
    ).upper()

    if method == "DELETE":

        if course.grades:

            return (
                "Cannot delete this course because "
                "grades are assigned to the course.",
                400
            )

        db.session.delete(course)
        db.session.commit()

        return redirect(
            url_for("web.courses")
        )

    if method in ["PUT", "PATCH"]:

        name = request.form.get("name")
        code = request.form.get("code")

        if not name or not code:
            return "Course name and code are required", 400

        existing_course = Course.query.filter(
            Course.code == code,
            Course.id != id
        ).first()

        if existing_course:
            return "Course code already exists", 409

        course.name = name
        course.code = code

        db.session.commit()

        return redirect(
            url_for("web.courses")
        )

    return "Invalid method", 400


# ================================
# GRADES
# ================================

@web_bp.route("/grades")
def grades():

    grade_list = Grade.query.all()

    return render_template(
        "grades/list.html",
        grades=grade_list
    )


@web_bp.route("/grades/new")
def new_grade():

    students = Student.query.all()
    courses = Course.query.all()

    return render_template(
        "grades/form.html",
        students=students,
        courses=courses
    )


@web_bp.route("/grades", methods=["POST"])
def create_grade():

    student_id = request.form.get(
        "student_id",
        type=int
    )

    course_id = request.form.get(
        "course_id",
        type=int
    )

    score = request.form.get(
        "score",
        type=float
    )

    if student_id is None:
        return "Student is required", 400

    if course_id is None:
        return "Course is required", 400

    if score is None:
        return "Score is required", 400

    if score < 0 or score > 100:
        return "Score must be between 0 and 100", 400

    student = db.session.get(
        Student,
        student_id
    )

    if not student:
        return "Student not found", 404

    course = db.session.get(
        Course,
        course_id
    )

    if not course:
        return "Course not found", 404

    grade = Grade(
        student_id=student_id,
        course_id=course_id,
        score=score
    )

    db.session.add(grade)
    db.session.commit()

    return redirect(
        url_for("web.grades")
    )


@web_bp.route("/grades/<int:id>/edit")
def edit_grade(id):

    grade = db.session.get(
        Grade,
        id
    )

    if not grade:
        return "Grade not found", 404

    return render_template(
        "grades/form.html",
        grade=grade
    )


@web_bp.route(
    "/grades/<int:id>",
    methods=["POST"]
)
def modify_grade(id):

    grade = db.session.get(
        Grade,
        id
    )

    if not grade:
        return "Grade not found", 404

    method = request.form.get(
        "_method",
        ""
    ).upper()

    if method == "DELETE":

        db.session.delete(grade)
        db.session.commit()

        return redirect(
            url_for("web.grades")
        )

    if method in ["PUT", "PATCH"]:

        score = request.form.get(
            "score",
            type=float
        )

        if score is None:
            return "Score is required", 400

        if score < 0 or score > 100:
            return "Score must be between 0 and 100", 400

        grade.score = score

        db.session.commit()

        return redirect(
            url_for("web.grades")
        )

    return "Invalid method", 400


# ================================
# ANALYTICS
# ================================

@web_bp.route("/analytics")
def analytics_page():

    # Get filter values from URL
    student_id = request.args.get(
        "student_id",
        type=int
    )

    course_id = request.args.get(
        "course_id",
        type=int
    )

    # Start with all grades
    query = Grade.query

    # Apply student filter
    if student_id:

        query = query.filter_by(
            student_id=student_id
        )

    # Apply course filter
    if course_id:

        query = query.filter_by(
            course_id=course_id
        )

    grades = query.all()

    # Get students and courses for filter display
    students = Student.query.all()
    courses = Course.query.all()

    # No matching grades
    if not grades:

        return render_template(
            "analytics/dashboard.html",

            statistics={
                "mean": 0,
                "median": 0,
                "standard_deviation": 0
            },

            course_average=[],

            ranking=[],

            students=students,

            courses=courses
        )


    # ================================
    # STATISTICS
    # ================================

    scores = [
        float(grade.score)
        for grade in grades
    ]

    mean = sum(scores) / len(scores)

    sorted_scores = sorted(scores)

    n = len(sorted_scores)

    if n % 2 == 1:

        median = sorted_scores[n // 2]

    else:

        median = (
            sorted_scores[n // 2 - 1]
            + sorted_scores[n // 2]
        ) / 2

    variance = sum(
        (score - mean) ** 2
        for score in scores
    ) / len(scores)

    standard_deviation = variance ** 0.5


    # ================================
    # COURSE AVERAGES
    # ================================

    course_average = []

    course_ids = set(
        grade.course_id
        for grade in grades
    )

    for course_id_value in course_ids:

        course = db.session.get(
            Course,
            course_id_value
        )

        course_grades = [
            grade
            for grade in grades
            if grade.course_id == course_id_value
        ]

        if course and course_grades:

            average = sum(
                float(grade.score)
                for grade in course_grades
            ) / len(course_grades)

            course_average.append({
                "course_id": course.id,
                "course_name": course.name,
                "average_score": round(
                    average,
                    2
                )
            })


    # ================================
    # RANKING
    # ================================

    ranking = []

    sorted_grades = sorted(
        grades,
        key=lambda grade: grade.score,
        reverse=True
    )

    for position, grade in enumerate(
        sorted_grades,
        start=1
    ):

        ranking.append({
            "rank": position,

            "student_name": (
                grade.student.name
                if grade.student
                else "Unknown"
            ),

            "course_name": (
                grade.course.name
                if grade.course
                else "Unknown"
            ),

            "score": float(
                grade.score
            )
        })


    return render_template(
        "analytics/dashboard.html",

        statistics={
            "mean": round(mean, 2),

            "median": round(
                median,
                2
            ),

            "standard_deviation": round(
                standard_deviation,
                2
            )
        },

        course_average=course_average,

        ranking=ranking,

        students=students,

        courses=courses
    )