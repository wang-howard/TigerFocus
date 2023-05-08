import sys
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
from .common import generate_course_id, generate_assignment_id
from .common import get_time
from . import bp
from .. import db
from ..models import User, Course, Assignment

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
                            user_netid=netid,
                            is_public=False,
                            last_updated=get_time())
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
        edited_course.last_updated = get_time()

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

@bp.route("/toggleexportcourse", methods=["GET", "POST"])
@login_required
def toggle_export_course():
    try:
        id = request.form.get("export_course")
        course = Course.query.get(id)
        course.is_public = not course.is_public
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
        course.last_updated = get_time()
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
        Course.query.get(course_id).last_updated = get_time()

        db.session.commit()

        if(user.user_type == "student"):
            return redirect(url_for(".hub"))
        else:
            return redirect(url_for(".instructor_view_assignments",
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

        Course.query.get(course_id).last_updated = get_time()

        db.session.commit()

        user = User.query.get(session["netid"])
        if user.user_type == "student":
            return redirect(url_for(".hub"))
        elif user.user_type == "instructor":
            return redirect(url_for(".instructor_view_assignments",
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
    id = request.form.get("id")
    assignment = Assignment.query.get(id)
    html = ""
    if assignment.status == 0:
        assignment.status = 1
        html = \
        f"""
        <button class="action-button-half">
          in progress
        </button>
        <input hidden name="id" value="{id}" />
        """
    elif assignment.status == 1:
        assignment.status = 2
        html = \
        f"""
        <button class="action-button-full">
          done
        </button>
        <input hidden name="id" value="{id}" />
        """
    else:
        assignment.status = 0
        html = \
        f"""
        <button class="action-button-empty">
          not started
        </button>
        <input hidden name="id" value="{id}" />
        """
    db.session.commit()
    return html

@bp.route("/instructorviewassignments", methods=["GET", "POST"])
@login_required
def instructor_view_assignments():
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
            due = a.due_date.strftime("%b %d %I:%M %p")
            assignment_data.append({"status": a.status,
                                    "id": a.id,
                                    "title": a.title,
                                    "due_date": due,
                                    "course_code": course.course_code,
                                    "color": course.color})
        return render_template("instructorviewassignments.html",
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
        new_assignment = Assignment(id=assignment_id,
                                    title=title,
                                    due_date=due,
                                    course_id=course_id)
        db.session.add(new_assignment)
        db.session.commit()

        return redirect(url_for(".instructor_view_assignments", courseid=course_id))
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)
