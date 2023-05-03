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
from app import cas_client
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

        # create list of dicts containing course information
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
                                   message = "undefined user type")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/createcourse", methods=["GET", "POST"])
@login_required
def created_course():
    """
    Receives form response with course information and creates Course
    object to commit to database.
    """
    netid = session["netid"]
    try:
       
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        netid = session["netid"]
        course_id = str(random.randint(0, 999999)).zfill(6)
        while True:
            query = Course.query.get(course_id)
            if query == None:
                break
            else:
                course_id = str(random.randint(0, 999999)).zfill(6)
        new_course = Course(id=course_id, course_code=course_code,
                            course_name=course_name, color=course_color,
                            user_netid=netid)
        user = User.query.get(netid)
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
    """
    Receives form response with course information and change requests
    and updates course object with new values
    """
    netid = session["netid"]
    try:
        user = User.query.get(netid)
        if user.user_type == "student":
            course_id = request.form.get("edited_course_id")
        elif user.user_type == "instructor":
            course_id = request.form.get("instructor_edited_course_id")
    
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        
        
        edited_course = Course.query.get(course_id)
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
@login_required
def delete_course():
    """
    Receives course ID from form response and search database to remove
    target course from courses database as well as linked assignments
    """
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
        user = User.query.get(netid)

        is_staff = True
        if user.user_type == "student":
            is_staff = False

        id = request.form.get("export_course")
        course = Course.query.get(id)

        course_code = course.course_code
        course_name = course.course_name
        assignments = course.assignments
        
        query_course = Public_Course.query.get(id)
        if query_course != None:
            query_course.course_code = course_code
            query_course.course_name = course_name
            query_course.assignments = assignments
        else:
            query_course = Public_Course(id=id,
                                            author = netid,
                                            show_author=True,
                                            staff_cert=is_staff,
                                            course_code=course_code,
                                            course_name=course_name,
                                            last_updated=date.today())
            db.session.add(query_course)

        assignments = list(course.assignments)
        for assignment in assignments:
            new_assignment_id = str(random.randint(0, 999999)).zfill(6)
            while True:
                query = Assignment.query.get(new_assignment_id)
                if query == None:
                    break
                else:   
                    new_assignment_id = str(random.randint(0, 999999)).zfill(6)

            public_assignment = Public_Assignment(
                                        id=new_assignment_id,
                                        title=assignment.title,
                                        due_date=assignment.due_date,
                                        course_id=id)
            db.session.add(public_assignment)
        
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
            print(ex, file=sys.stderr)
            return render_template("error.html", message=ex)

@bp.route("/instructorexportcourses", methods=["GET", "POST"])
@login_required
def instructor_export_courses():
    try:
        course_ids = request.form.get('selected_courses')
        if course_ids == '':
            return redirect(url_for(".hub"))
        
        course_list = course_ids.split(",")
        netid = session["netid"]
        user = User.query.get(netid)

        for id in course_list:
            is_staff = True
            if user.user_type == "student":
                is_staff = False

            course = Course.query.get(id)
            course_code = course.course_code
            course_name = course.course_name
            assignments = course.assignments

            new_course_id = str(random.randint(0, 999999)).zfill(6)
            while True:
                query = Public_Course.query.get(new_course_id)
                if query is None:
                    break
                else:
                    new_course_id = str(random.randint(0, 999999)).zfill(6)

            exported_course = Public_Course(id=new_course_id,
                                            author = netid,
                                            show_author = True,
                                            staff_cert = is_staff,
                                            course_code=course_code,
                                            course_name=course_name,
                                            last_updated=date.today())

            db.session.add(exported_course)

            assignments = list(course.assignments)
            for assignment in assignments:

                new_assignment_id = str(random.randint(0, 999999)).zfill(6)

                while True:
                    query = Public_Assignment.query.get(new_assignment_id)
                    if query == None:
                        break
                    else:
                        new_assignment_id = str(random.randint(0, 999999)).zfill(6)

                public_assignment = Public_Assignment(
                                        id=new_assignment_id,
                                        title=assignment.title,
                                        due_date=assignment.due_date,
                                        course_id=new_course_id)
                db.session.add(public_assignment)

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
        # when nothing is selected to be imported this is where we catch
        if course_ids == '':
            return redirect(url_for(".preloaded"))

        course_list = course_ids.split(",")
        netid = session["netid"]
        user = User.query.get(netid)

        for id in course_list:
            course = Public_Course.query.get(id)
            course_code = course.course_code
            course_name = course.course_name
            assignments = course.assignments

            new_id = str(random.randint(0, 999999)).zfill(6)
            while True:
                query = Course.query.get(new_id)
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
                    query = Assignment.query.get(assignment_id)
                    if query is None:
                        break
                    else:
                        assignment_id = str(random.randint(0, 999999)).zfill(6)

                import_assignment = Assignment(id=assignment_id,
                                               title=a.title,
                                               due_date=a.due_date,
                                               status=None,
                                               course_id=new_id)
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
            query = Assignment.query.get(assignment_id)
            if query == None:
                break
            else:
                assignment_id = str(random.randint(0, 999999)).zfill(6)
        assignment = Assignment(id=assignment_id, title=title,
                                due_date=due, status=None,
                                course_id=course_id)
        db.session.add(assignment)
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/instructoraddassignment", methods=["GET", "POST"])
@login_required
def instructor_add_assignment():
    try:
        
        course_id = request.form.get("current_id")        
        due = request.form.get("due_date")
        title = request.form.get("title")

        assignment_id = str(random.randint(0, 999999)).zfill(6)
        while True:
            query = Assignment.query.get(assignment_id)
            if query == None:
                break
            else:
                assignment_id = str(random.randint(0, 999999)).zfill(6)
        new_assignment = Assignment(id=assignment_id, title=title,
                                due_date=due, status=False,
                                course_id=course_id)
        db.session.add(new_assignment)
        db.session.commit()

        return redirect(url_for(".assignment", courseid=course_id))
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
        user = User.query.get(netid)

        edited_assignment = Assignment.query.get(assignment_id)
        edited_assignment.due_date = due
        edited_assignment.title = title
        edited_assignment.user_netid = netid
        course_id = edited_assignment.course_id

        db.session.commit()

        if(user.user_type == "Student"):
            return redirect(url_for(".hub"))
        else:
            return redirect(url_for(".assignment", courseid=course_id))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/deleteassignment", methods=["GET", "POST"])
@login_required
def delete_assignment():
    try:
        id = request.form.get("assignment_id")
        assignment = Assignment.query.get(id)
        course_id = assignment.course_id
        Assignment.query.filter_by(id=id).delete()

        db.session.commit()

        user = User.query.get(session["netid"])
        if user.user_type == "student":
            return redirect(url_for(".hub"))
        elif user.user_type == "instructor":
            return redirect(url_for(".assignment", courseid=course_id))
        else:
            return render_template("error.html",
                                   message="User type error when \
                                    deleting assignment")
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/statusassignment", methods=["GET", "POST"])
@login_required
def status_assignment():
    try:
        status = request.form.get("status")
        id = request.form.get("id")
        assignment = Assignment.query.get(id)
        if status == "FALSE":
            assignment.status = False
        elif status == "TRUE":
            assignment.status = True
        else:
            assignment.status = None
        
        db.session.commit()

        return redirect(url_for(".hub"))
      
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/preloaded")
def preloaded():
    netid = session["netid"]
    user = User.query.get(netid)
    first = user.first_name
    
    return render_template("preloaded.html",
                           first_name=first, 
                           user_type=user.user_type)


@bp.route("/searchpreloaded")
def searchpreloaded():
    title = request.args.get('title')
    code = request.args.get('code')
    title = "%{}%".format(title)
    code = "%{}%".format(code)
    courses = Public_Course.query.filter(Public_Course.course_name.ilike(title)).filter(Public_Course.course_code.ilike(code))

    # create list of dict of course codes
    course_codes = []
    course_ids = []

    for course in courses:
        id = course.id
        author = course.author
        show_author = course.show_author
        staff_cert = course.staff_cert
        course_code = course.course_code
        course_name = course.course_name
        last_updated = course.last_updated.strftime("%b %d, %Y")

        course_codes.append({"course_code": course_code,
                             "course_name": course_name,
                             "author": author,
                             "show_author": show_author,
                             "staff_cert": staff_cert,
                             "id": id,
                             "last_updated": last_updated})
        course_ids.append(course.id)

    return render_template("searchpreloaded.html",
                           courses=course_codes)

@bp.route("/assignment", methods=["GET", "POST"])
@login_required
def assignment():
    netid = session["netid"]
    try:
        user = User.query.get(netid)
        first = user.first_name
        id = request.args.get("courseid")
        
        assignments = Assignment.query.filter_by(course_id=id)\
                            .order_by(Assignment.due_date).all()
        
        assignment_data = []
        course = Course.query.get(id)
        course_code = course.course_code
        for a in assignments:
            due = a.due_date.strftime("%b %d, %Y %I:%M %p")
            assignment_data.append({"status": a.status,
                                    "id": a.id,
                                    "title": a.title,
                                    "due_date": due,
                                    "course_code": course.course_code,
                                    "color": course.color})
        return render_template("assignment.html",
                               first_name=first,
                               assignments=assignment_data, 
                               course_code=course_code,
                               id=id)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/preloadedassignment", methods=["GET", "POST"])
@login_required
def preloadedassignment():
    netid = session["netid"]
    try:
        user = User.query.get(netid)
        first = user.first_name
        id = request.args.get("courseid")
        print(id)

        
        assignments = Public_Assignment.query.filter_by(course_id=id)\
                            .order_by(Public_Assignment.due_date).all()
        
        assignment_data = []
        course = Public_Course.query.get(id)
        course_code = course.course_code
        author = course.author
        for a in assignments:
            due = a.due_date.strftime("%b %d, %Y %I:%M %p")
            assignment_data.append({
                                    "id": a.id,
                                    "title": a.title,
                                    "due_date": due,
                                    "course_code": course.course_code})
        return render_template("preloadedassignment.html",
                               author=author,
                               assignments=assignment_data, 
                               course_code=course_code,
                               id=id)
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
