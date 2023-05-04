import sys, random
from datetime import date, datetime
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
from .common import generate_course_id, generate_assignment_id
from . import bp
from .. import db
from ..models import User, Course, Assignment, Public_Course, Public_Assignment

@bp.route("/createcourse", methods=["GET", "POST"])
@login_required
def create_course():
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
        course_id = generate_course_id()
        new_course = Course(id=course_id,
                            course_code=course_code,
                            course_name=course_name,
                            color=course_color,
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
    try:
        course_id = request.form.get("edited_course_id")\
            if User.query.get(session["netid"]).user_type == "student"\
            else request.form.get("instructor_edited_course_id")

        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")

        edited_course = Course.query.get(course_id)
        edited_course.course_code = course_code
        edited_course.course_name = course_name
        edited_course.color = course_color

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
        id = request.form.get("export_course")
        course = Course.query.get(id)
        course.is_public = True
        course.last_updated = datetime.now()
        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
            print(ex, file=sys.stderr)
            return render_template("error.html", message=ex)

@bp.route("/addassignment", methods=["GET", "POST"])
@login_required
def add_assignment():
    try:
        course_id = request.form.get("course_id")
        due = request.form.get("due_date")
        title = request.form.get("title")
        course = Course.query.get(course_id)

        assignment_id = generate_assignment_id()
        assignment = Assignment(id=assignment_id, title=title,
                                due_date=due, status=None,
                                course_id=course_id)
        course.assignments.append(assignment)
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
        netid = session["netid"]
        user = User.query.get(netid)

        assignment_id = request.form.get("edited_assignment_id")
        due = request.form.get("due_date")
        title = request.form.get("title")

        edited_assignment = Assignment.query.get(assignment_id)
        edited_assignment.due_date = due
        edited_assignment.title = title
        course_id = edited_assignment.course_id

        db.session.commit()

        if(user.user_type == "student"):
            return redirect(url_for(".hub"))
        else:
            return redirect(url_for(".instructor_assignments",
                                    courseid=course_id))
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
            return redirect(url_for(".instructor_assignments",
                                    courseid=course_id))
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
        id = request.form.get("id")
        assignment = Assignment.query.get(id)
        if assignment.status == 0:
            assignment.status = 1
        elif assignment.status == 1:
            assignment.status = 2
        else:
            assignment.status = 0

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
            course = Course.query.get(id)
            course.is_public = True
            course.last_updated = datetime.now()
            db.session.commit()

        return redirect(url_for(".hub"))
    except Exception as ex:
            print(ex, file=sys.stderr)
            return render_template("error.html", message=ex)

@bp.route("/instructorassignments", methods=["GET", "POST"])
@login_required
def instructor_assignments():
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
        return render_template("instructorassignments.html",
                               first_name=first,
                               assignments=assignment_data, 
                               course_code=course_code,
                               id=id)
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

        assignment_id = generate_assignment_id()
        new_assignment = Assignment(id=assignment_id, title=title,
                                due_date=due, status=False,
                                course_id=course_id)
        db.session.add(new_assignment)
        db.session.commit()

        return redirect(url_for(".instructor_assignments", courseid=course_id))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
