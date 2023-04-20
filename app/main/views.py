"""
File contains all view functions to route and reroute client requests
for the flask App. This file represents the bulk of the application,
including processing requests and interfacing with the database.
"""

import sys, random
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
from app import cas_client
from . import bp
from .. import db
from ..models import User, Course, Assignment, Public_Course, Public_Assignment
import urllib 
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
        return render_template("error.html", message=ex )

@bp.route("/createcourse", methods=["GET", "POST"])
@login_required
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
@login_required
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

@bp.route("/deletecourse", methods=["GET", "POST"])
def delete_course():
    try:
        id = request.form.get("course_del_id")
        course = Course.query.get(id)

        assignments = list(course.assignments)
        for assignment in assignments:
            db.session.delete(assignment)
                 
        Course.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/exportcourse", methods=["GET", "POST"])
@login_required
def export_course():
    try:
        netid = session["netid"]
        user = User.query.filter_by(netid=netid).first()
        #first = user.first_name

        is_staff = True
        if user.user_type == "student":
            is_staff = False

        id = request.form.get("export_course")
        course = Course.query.get(id)
        course_code = course.course_code
        course_name = course.course_name
        assignments = course.assignments

        assignments = list(course.assignments)
        for assignment in assignments:
            public_assignment = Public_Assignment(id=assignment.id, title=assignment.title,
                                due_date=assignment.due_date,course_id=assignment.course_id)
            db.session.add(public_assignment)

        exported_course = Public_Course(id=id, author = netid, show_author = True,
                                 staff_cert = is_staff, course_code=course_code,
                                 course_name=course_name)
        
        db.session.add(exported_course)
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
            print(ex, file=sys.stderr)
            return render_template("error.html", message=ex)
    
@bp.route("/importcourses", methods=["GET", "POST"])
@login_required
def import_courses():
    try:
        
        course_ids = request.form.get('selected_courses')

        course_list = course_ids.split(",")
        netid = session["netid"]
        user = User.query.filter_by(netid=netid).first()

        for id in course_list:
        
            course = Public_Course.query.get(id)
            course_code = course.course_code
            course_name = course.course_name
            assignments = course.assignments

            new_id = str(random.randint(0, 999999)).zfill(6)
            while True:
                query = Course.query.filter_by(id=new_id).first()
                if query is None:
                    break
                else:
                    new_id = str(random.randint(0, 999999)).zfill(6)
            
            new_course = Course(id=new_id, course_code=course_code,
                                course_name=course_name, color="#FFC78F",
                                user_netid=netid)
            user.courses.append(new_course)
            db.session.add(new_course)
            # commit so new_course exists before assignments are added to it
            db.session.commit()

            assignments = list(course.assignments)
            for a in assignments:
                assignment_id = str(random.randint(0, 999999)).zfill(6)
                while True:
                    query = Assignment.query.filter_by(id=assignment_id).first()
                    if query is None:
                        break
                    else:
                        assignment_id = str(random.randint(0, 999999)).zfill(6)

                import_assignment = Assignment(id=assignment_id, title=a.title,
                                        due_date=a.due_date, status=False,
                                        course_id=new_id)
                print(import_assignment)
                db.session.add(import_assignment)
        
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
            print(ex, file=sys.stderr)
            return render_template("error.html", message=ex)

@bp.route("/addassignment", methods=["GET", "POST"])
@login_required
def add_assignment():
    try:
        course = request.form.get("course_code")
        due = request.form.get("due_date")
        title = request.form.get("title")
        netid = session["netid"]
        db_course = Course.query \
            .filter(Course.course_code==course) \
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
@login_required
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
@login_required
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
    
@bp.route("/preloaded")
def preloaded():
    
    netid = session["netid"]
    user = User.query.filter_by(netid=netid).first()
    first = user.first_name
    courses = Public_Course.query.all()

    # create list of dict of course codes and their colors
    course_codes = []
    course_ids = []
    
    for course in courses:
        id = course.id
        author = course.author
        show_author = course.show_author
        staff_cert = course.staff_cert
        course_code = course.course_code
        course_name = course.course_name
        
        course_codes.append({"course_code": course_code,
                             "course_name": course_name ,
                             "author": author ,
                             "show_author": show_author ,
                             "staff_cert": staff_cert ,
                             "id": id })
        course_ids.append(course.id)
    

    return render_template("preloaded.html", first_name=first, courses=course_codes)


@bp.route("/timer")
def timer():
    style = url_for('static', filename='css/timerStyles.css')
    id = "pomodoro-app"
    link = "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1"
    script = url_for('static', filename='script/timer.js')

    return render_template("timer.html", style=style, id=id, mins=25,
                           source=link, script=script )

@bp.route("/about")
def about():
    
    return render_template("about.html" )

@bp.route("/shortBreak")
def shortBreak():
    id = "short-app"
    link = "https://www.youtube.com/embed/g1WfKpFQdOg?autoplay=1&mute=1"
    style = url_for('static', filename='css/shortbreakStyles.css')
    script = url_for('static', filename='script/shortBreak.js')
    return render_template("timer.html", style=style, id=id, mins=5,
                           source=link, script=script)

@bp.route("/longBreak")
def longBreak():
    style = url_for('static', filename='css/longbreakStyles.css')
    id = "long-app"
    link = "https://www.youtube.com/embed/FqKjFMr28rA?autoplay=1&mute=1"
    script = url_for('static', filename='script/longBreak.js')
    return render_template("timer.html", style=style, id=id, mins=15,
                           source=link, script=script)


@bp.route('/start', methods=['POST'])
@login_required
def start_session():
    try:
        # get all checked checkboxes
        checkboxes = request.form.get('selected_assignments')
        style = url_for('static', filename='css/timerStyles.css')
        id = "pomodoro-app"
        link = "https://www.youtube.com/embed/Kz1QJ4-lerk?autoplay=1&mute=1"
        script = url_for('static', filename='script/timer.js')

        # create an array to store the titles of the checked assignments
        
        # redirect the user to the timer.html page with the selected assignments as a query parameter
        #selected_assignments_query_param = urllib.parse.quote(selected_assignments_str)
        return render_template("timer.html", assignments = checkboxes, style=style, id=id, mins=25,
                           source=link, script=script )

    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/admincourse")
@login_required
def admincourse():
    netid = session["netid"]
    user = User.query.filter_by(netid=netid).first()
    first = user.first_name

    return render_template("admincourse.html", first_name = first)

@bp.route("/assignment")
@login_required
def assignment():
    netid = session["netid"]
    user = User.query.filter_by(netid=netid).first()
    first = user.first_name

    return render_template("assignment.html", first_name = first)

@bp.route("/mainPage")
def mainPage():
    return render_template("mainPage.html")
from flask import Flask, request, render_template

app = Flask(__name__)

