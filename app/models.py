"""
This file contains the Flask-SQLAlchemy models created to connect and
interface with the PostgresSQL database. Models represents the 
"""

from app import db
from flask_login import UserMixin
from datetime import datetime, timezone
from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    netid = db.Column(db.String, primary_key=True, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    user_type = db.Column(db.String, nullable=False)
    courses = db.relationship("Course", backref="user", lazy="dynamic")

    def __repr__(self):
        return self.first_name + " " + self.last_name + " (" +\
            self.netid + ")"
    
    def get_id(self):
        return str(self.netid)

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    course_code = db.Column(db.String, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False) 
    user_netid = db.Column(db.String, db.ForeignKey("users.netid"))
    is_public = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime,
                             default=datetime.now(timezone.utc))
    assignments = db.relationship("Assignment", backref="course",
                                  order_by="asc(Assignment.due_date)",
                                  lazy="dynamic")

    def __repr__(self):
        return self.course_code + ": " + self.course_name + " (" +\
            str(self.id) + ")"
    
class Assignment(db.Model):
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, default=0)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    def __repr__(self):
        return self.title + " (" + str(self.id) + ")"

@login_manager.user_loader
def load_user(netid):
    return User.query.get(netid)