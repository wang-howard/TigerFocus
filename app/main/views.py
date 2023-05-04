"""
File contains all view functions to route and reroute client requests
for the flask App. This file represents the bulk of the application,
including processing requests and interfacing with the database.
"""

import sys, random
from datetime import date
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
from . import bp
from .. import db
from ..models import User, Course, Assignment, Public_Course, Public_Assignment

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

@bp.route("/hub")
@login_required
def hub():
    """
    Main application hub displays each user's indiviudal assignment and
    course information. Majority of functionality found in html/css/js.
    """
    netid = session["netid"]
    try:
        user = User.query.get(netid)
        first = user.first_name
        courses = list(user.courses)
        
        # create list of dict of course info and their colors
        course_data = []
        course_ids = []
        for course in courses:
            color = course.color
            code = course.course_code
            id = course.id
            name = course.course_name
            course_data.append({"course_code": code,
                                 "course_name": name,
                                 "color": color,
                                 "id": id})
            course_ids.append(course.id)

        # create list of dicts containing assignment information
        assignments = Assignment.query.filter(Assignment.course_id\
                        .in_(course_ids))\
                        .order_by(Assignment.due_date).all()
        assignment_data = []
        for a in assignments:
            course = Course.query.get(a.course_id)
            date = a.due_date.strftime("%b %d, %Y")
            time = a.due_date.strftime("%I:%M %p")
            assignment_data.append({"status": a.status,
                                    "id": a.id,
                                    "title": a.title,
                                    "date": date,
                                    "time": time,
                                    "course_code":course.course_code,
                                    "color": course.color})

        if user.user_type == "student":
            return render_template("studenthub.html",
                                   first_name=first,
                                   courses=course_data,
                                   assignments=assignment_data)
        elif user.user_type == "instructor":
            return render_template("instructorhub.html",
                                   first_name=first,
                                   courses=course_data,
                                   assignments=assignment_data)
        else:
            return render_template("error.html",
                                   message="undefined user type")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/start", methods=["POST"])
@login_required
def start_session():
    try:
        # get all checked checkboxes
        checkboxes = request.form.get("selected_assignments")
        style = url_for("static", filename="css/timerStyles.css")
        id = "pomodoro-app"
        link = "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1"
        script = url_for("static", filename="script/timer.js")
        return render_template("timer.html",
                               assignments=checkboxes,
                               style=style,
                               id=id, mins=25,
                               source=link, script=script)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/timer")
def timer():
    style = url_for("static", filename="css/timerStyles.css")
    id = "pomodoro-app"
    link = "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1"
    script = url_for("static", filename="script/timer.js")

    return render_template("timer.html", style=style, id=id, mins=25,
                           source=link, script=script )

@bp.route("/shortBreak")
def shortBreak():
    id = "short-app"
    link = "https://www.youtube.com/embed/g1WfKpFQdOg?autoplay=1&mute=1"
    style = url_for("static", filename="css/shortbreakStyles.css")
    script = url_for("static", filename="script/shortBreak.js")
    return render_template("timer.html", style=style, id=id, mins=5,
                           source=link, script=script)

@bp.route("/longBreak")
def longBreak():
    style = url_for("static", filename="css/longbreakStyles.css")
    id = "long-app"
    link = "https://www.youtube.com/embed/FqKjFMr28rA?autoplay=1&mute=1"
    script = url_for("static", filename="script/longBreak.js")
    return render_template("timer.html", style=style, id=id, mins=15,
                           source=link, script=script)

@bp.route("/about")
def about():
    return render_template("about.html")
