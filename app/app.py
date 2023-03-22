"""
RUN THESE COMMANDS ON STARTUP:
    export DB_URI=postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com/tigerfocus_4gqq
    export SEC_KEY=tigerFocus098098
"""

import os, enum, random
from datetime import date, datetime
from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SEC_KEY")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap = Bootstrap(app)

class Color(enum.Enum):
    RED = "RED"
    ORANGE = "ORANGE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    BLUE = "BLUE"
    CYAN = "CYAN"
    PINK = "PINK"
    PURPLE = "PURPLE"

class Role(enum.Enum):
    student = 0
    admin = 1

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_type = db.Column(db.Enum(Role))
    courses = db.relationship('Course', backref="user", lazy="dynamic")

    def __repr__(self):
        return self.first_name + " " + self.last_name + " (" +\
            str(self.id) + ")"

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    course_code = db.Column(db.String)
    course_name = db.Column(db.String)
    color = db.Column(db.Enum(Color))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assignments = db.relationship("Assignment", backref="course",
                                  lazy="dynamic")

    def __repr__(self):
        return self.course_code + ": " + self.course_name + " (" +\
            str(self.id) + ")"
    
class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.Boolean)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    def __repr__(self):
        return self.title + " (" + str(self.id) + ")"

class SelectIDForm(FlaskForm):
    user_id = SelectField("Select PUID", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET"])
def index():
    try:
        users = User.query.all()
        print(users)
        user_data = []
        if not users:
            users = []
        else:
            for user in users:
                user_data.append([user.id, user.first_name,
                                  user.last_name, user.user_type])
        return render_template("index.html", data=user_data)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/adduser")
def add_user():
    return render_template("register.html")

@app.route("/createduser", methods=["GET", "POST"])
def created_user():
    try:
        user_id = request.form.get("userid")
        first = request.form.get("first")
        last = request.form.get("last")

        new_user = User(id=user_id, first_name=first, last_name=last,
                        user_type=Role.student)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/selectuser", methods=["GET", "POST"])
def select_user():
    try:
        users = User.query.all()
        user_ids = []
        for user in users:
            user_ids.append(user.id)
        form = SelectIDForm()
        form.user_id.choices = user_ids
        if form.validate_on_submit():
            session["user_id"] = form.user_id.data
            return redirect(url_for("view_courses"))
        return render_template("selectuser.html", form=form)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/viewcourses", methods=["GET", "POST"])
def view_courses():
    user_id = session["user_id"]
    try:
        course_data = []
        user = User.query.filter_by(id=user_id).first()
        courses = user.courses
        return render_template("courses.html", userid=user_id,
                               courses=courses)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/addcourse", methods=["GET", "POST"])
def add_course():
    try:
        return render_template("addcourse.html")
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/createdcourse", methods=["GET", "POST"])
def created_course():
    try:
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        user_id = session["user_id"]
        course_id = str(random.randint(0, 999999)).zfill(6)
        while True:
            query = Course.query.filter_by(id=course_id).first()
            if query == None:
                break
            else:
                course_id = str(random.randint(0, 999999)).zfill(6)
        new_course = Course(id=course_id, course_code=course_code,
                            course_name=course_name, color=course_color,
                            user_id=user_id)
        user = User.query.filter_by(id=user_id).first()
        user.courses.append(new_course)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for("view_courses"))
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/hub")
def hub():
    user_id = session["user_id"]
    try:
        user = User.query.filter_by(id=user_id).first()
        courses = user.courses
        course_codes = []
        for course in courses:
            course_codes.append(course.course_code)
        return render_template("hub.html", user_id=user_id,
                               courses=course_codes)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/timer")
def timer():
    return render_template("timer.html")

@app.route("/longBreak")
def longBreak():
    return render_template("longBreak.html")

@app.route("/shortBreak")
def shortBreak():
    return render_template("shortBreak.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5554", debug=True)