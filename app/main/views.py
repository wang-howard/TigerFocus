"""
File contains all view functions to route and reroute client requests
for the flask App. This file represents the bulk of the application,
including processing requests and interfacing with the database.
"""

import sys, random
from flask import render_template, redirect, url_for
from flask import session, request
from app import cas_client
from . import bp
from .. import db
from ..models import User, Course, Assignment

@bp.route("/", methods=["GET"])
def index():
    """
    Renders homepage
    """
    try:
        return render_template("index.html")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/login", methods=["GET", "POST"])
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

@bp.route("/processlogin", methods=["GET", "POST"])
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
            return redirect(url_for(".hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/newuser", methods=["POST"])
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
    return redirect(url_for(".hub"))

@bp.route("/hub")
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
            id = course.id
            course_codes.append({"course_code": code,
                                 "color": color ,
                                 "id": id })
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

@bp.route("/createcourse", methods=["GET", "POST"])
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
        
        return redirect(url_for(".hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
@bp.route("/editcourse", methods=["GET", "POST"])
def edit_course():
    try:
        course_id = request.form.get("edited_course_id")
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        netid = session["netid"]
        
        edited_course = Course.query.filter_by(id=course_id).first()
        edited_course.course_code = course_code
        edited_course.course_name = course_name
        edited_course.color = course_color
        edited_course.user_netid = netid
        
        db.session.commit()
        
        return redirect(url_for(".hub"))
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
@bp.route("/addassignment", methods=["GET", "POST"])
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
        return redirect(url_for(".hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
    
@bp.route("/editassignment", methods=["GET", "POST"])
def edit_assignment():
    try:
        assignment_id = request.form.get("edited_assignment_id")
        due = request.form.get("due_date")
        title = request.form.get("title")
        netid = session["netid"]
        
        edited_assignment = Assignment.query.filter_by(id=assignment_id).first()
        edited_assignment.due_date = due
        edited_assignment.title = title
        edited_assignment.user_netid = netid
        
        db.session.commit()
        
        return redirect(url_for(".hub"))
        
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/deleteassignment", methods=["GET", "POST"])
def delete_assignment():
    try:
        id = request.form.get("assignment_id")
        print(id)
        Assignment.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/timer")
def timer():
    style = url_for('static', filename='css/timerStyles.css')
    id = "pomodoro-app"
    link = "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1"
    script = url_for('static', filename='script/timer.js')
    assignments = request.args.get('assignments')

    return render_template("timer.html", style=style, id=id, mins=25,
                           source=link, script=script, assignments=assignments)

@bp.route("/shortBreak")
def shortBreak():
    id = "short-app"
    link = "https://www.youtube.com/embed/g1WfKpFQdOg?autoplay=1&mute=1"
    style = url_for('static', filename='css/shortbreakStyles.css')
    script = url_for('static', filename='script/shortBreak.js')
    return render_template("timer.html", style=style, id=id, mins=25,
                           source=link, script=script)

@bp.route("/longBreak")
def longBreak():
    style = url_for('static', filename='css/longbreakStyles.css')
    id = "long-app"
    link = "https://www.youtube.com/embed/FqKjFMr28rA?autoplay=1&mute=1"
    script = url_for('static', filename='script/longBreak.js')
    return render_template("timer.html", style=style, id=id, mins=25,
                           source=link, script=script)

@bp.route("/mainPage")
def mainPage():
    return render_template("mainPage.html")
