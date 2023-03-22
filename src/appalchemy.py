"""
RUN THIS COMMAND FIRST:
    export DB_URI=postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com/tigerfocus_4gqq
"""

import os
import enum
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_URI = os.getenv("DB_URI")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class CourseColor(enum.Enum):
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
    courses = db.relationship('Course', backref="user")

    def __repr__(self):
        return self.first_name + " " + self.last_name + " (" +\
            str(self.id) + ")"

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    course_code = db.Column(db.String)
    course_name = db.Column(db.String)
    color = db.Column(db.Enum(CourseColor))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    assignments = db.relationship("Assignment", backref="course")

    def __repr__(self):
        return self.course_code + ": " + self.course_name + " (" +\
            str(self.id) + ")"
    
class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String)
    due_date = db.Column(db.Time)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    def __repr__(self):
        return self.title + " (" + str(self.id) + ")"
