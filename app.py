from flask import Flask, app

from config import Config
from extensions import db, jwt


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from models import User, Student, Course, Grade

    with app.app_context():
        db.create_all()

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from routes.students import students_bp
    app.register_blueprint(students_bp)

    from routes.courses import courses_bp
    app.register_blueprint(courses_bp)

    from routes.grades import grades_bp
    app.register_blueprint(grades_bp)

    from routes.analytics import analytics_bp
    app.register_blueprint(analytics_bp)

    from routes.web import web_bp
    app.register_blueprint(web_bp)

    from routes.reports import reports_bp
    app.register_blueprint(reports_bp)   

    from routes.student_view import student_view_bp
    app.register_blueprint(student_view_bp)

    return app


app = create_app()


@app.route("/")
def home():
    return "Student Performance Analytics System"


if __name__ == "__main__":
    app.run(debug=True)