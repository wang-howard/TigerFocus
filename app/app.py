"""
SET THESE ENVIRONMENT VARIABLES ON STARTUP:
export FLASK_APP=app/app.py
export DB_URI=postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com/tigerfocus_4gqq
export SEC_KEY=tigerFocus098098
export SERVICE_URL=http://localhost:5553/login?next=process_login
"""

import sys, os, random
from cas import CASClient
from flask import Flask, request, session
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Flask app configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SEC_KEY")

# Flask extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Princeton CAS Authentification client
cas_client = CASClient(version=3, service_url=os.getenv("SERVICE_URL"),
                       server_url="https://fed.princeton.edu/cas/")

"""
SQLAlchemy classes and enums
"""
class User(db.Model):
    __tablename__ = "users"
    netid = db.Column(db.String, primary_key=True, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_type = db.Column(db.String)
    courses = db.relationship("Course", backref="user", lazy="dynamic")

    def __repr__(self):
        return self.first_name + " " + self.last_name + " (" +\
            self.netid + ")"

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    course_code = db.Column(db.String)
    course_name = db.Column(db.String)
    color = db.Column(db.String)
    user_netid = db.Column(db.String, db.ForeignKey("users.netid"))
    assignments = db.relationship("Assignment", backref="course",
                                  order_by="asc(Assignment.due_date)",
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

"""
View Functions
"""
@app.route("/", methods=["GET"])
def index():
    """
    Renders homepage
    """
    try:
        return render_template("index.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Redirects to CAS authentification, which returns a ticket to
    validate. If successful, redirects to login prcoessing function.
    """
    try:
        next = request.args.get("next")
        ticket = request.args.get("ticket")
        if not ticket:
            # No ticket, request came from end user, send to CAS login
            cas_login_url = cas_client.get_login_url()
            print('CAS login URL: %s', cas_login_url)
            return redirect(cas_login_url)
        
        print('ticket: %s', ticket)
        print('next: %s', next)
        user, _, _ = cas_client.verify_ticket(ticket)
        if not user:
            return render_template("error.html",
                                   message="Failed to verify ticket")
        else:
            # Login successfully, redirect according "next" query parameter.
            session["netid"] = user
            return redirect(url_for(next))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@app.route("/processlogin", methods=["GET", "POST"])
def process_login():
    """
    If user is in database, redirects to hub. Otherwise, redirects to
    register page for name and role entry.
    """
    netid = session["netid"]
    try:
        if User.query.filter_by(netid=netid).first() is None:
            return render_template("register.html", netid=netid)
        else:
            return redirect(url_for("hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@app.route("/newuser", methods=["POST"])
def new_user():
    """
    Receives post form from register page and enters new user to
    database, then redirects to user's hub.
    """
    netid = request.form.get("netid")
    first = request.form.get("first")
    last = request.form.get("last")
    user_type = request.form.get("user_type")

    user = User(netid=netid, first_name=first, last_name=last,
                user_type=user_type)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("hub"))

@app.route("/hub")
def hub():
    """
    Main application hub displays each user's indiviudal assignment and
    course information. Majority of functionality found in html/css/js.
    """
    netid = session["netid"]
    try:
        user = User.query.filter_by(netid=netid).first()
        first = user.first_name
        courses = list(user.courses)
        
        # create list of dict of course codes and their colors
        course_codes = []
        course_ids = []
        for course in courses:
            color = course.color
            code = course.course_code
            course_codes.append({"course_code": code,
                                 "color": color })
            course_ids.append(course.id)

        # create list of dicts containing course information
        assignments = Assignment.query.filter(Assignment.course_id\
                        .in_(course_ids))\
                        .order_by(Assignment.due_date).all()
        assignment_data = []
        for a in assignments:
            course = Course.query.filter_by(id=a.course_id).first()
            assignment_data.append({"status": a.status,
                                    "id": a.id,
                                    "title": a.title,
                                    "due_date": a.due_date,
                                    "course_code":course.course_code,
                                    "color": course.color})
        return render_template("hub.html", first_name=first,
                               courses=course_codes,
                               assignments=assignment_data)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@app.route("/viewcourses", methods=["GET", "POST"])
def view_courses():
    netid = session["netid"]
    try:
        course_data = []
        user = User.query.filter_by(id=netid).first()
        courses = user.courses
        return render_template("courses.html", userid=netid,
                               courses=courses)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@app.route("/createcourse", methods=["GET", "POST"])
def created_course():
    try:
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        netid = session["netid"]
        course_id = str(random.randint(0, 999999)).zfill(6)
        while True:
            query = Course.query.filter_by(id=course_id).first()
            if query == None:
                break
            else:
                course_id = str(random.randint(0, 999999)).zfill(6)
        new_course = Course(id=course_id, course_code=course_code,
                            course_name=course_name, color=course_color,
                            user_netid=netid)
        user = User.query.filter_by(netid=netid).first()
        user.courses.append(new_course)
        db.session.add(new_course)
        db.session.commit()
        
        return redirect(url_for("hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
@app.route("/addassignment", methods=["GET", "POST"])
def add_assignment():
    try:
        course = request.form.get("course_code")
        due = request.form.get("due_date")
        title = request.form.get("title")
        netid = session["netid"]
        db_course = Course.query\
            .filter(Course.course_code==course)\
            .filter(Course.user_netid==netid).first()
        course_id = db_course.id
        assignment_id = str(random.randint(0, 999999)).zfill(6)
        while True:
            query = Assignment.query.filter_by(id=assignment_id).first()
            if query == None:
                break
            else:
                assignment_id = str(random.randint(0, 999999)).zfill(6)
        assignment = Assignment(id=assignment_id, title=title,
                                due_date=due, status=False,
                                course_id=course_id)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for("hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@app.route("/deleteassignment", methods=["GET", "POST"])
def delete_assignment():
    try:
        id = request.form.get("assignment_id")
        print(id)
        Assignment.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for("hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
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

@app.route("/mainPage")
def mainPage():
    return render_template("mainPage.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5553", debug=True)