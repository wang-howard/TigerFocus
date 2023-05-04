import sys
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
from .common import generate_course_id, generate_assignment_id
from . import bp
from .. import db
from ..models import User, Course, Assignment

@bp.route("/publiccourses")
def public_courses():
    try:
        netid = session["netid"]
        user = User.query.get(netid)
        first = user.first_name
        
        return render_template("publiccourses.html",
                            first_name=first, 
                            user_type=user.user_type)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/searchpubliccourses")
def search_public_courses():
    netid = session["netid"]
    user = User.query.get(netid)

    title = request.args.get("title")
    code = request.args.get("code")
    title = "%{}%".format(title)
    code = "%{}%".format(code)
    courses = Course.query\
                .filter_by(is_public=True)\
                .filter(Course.course_name.ilike(title))\
                .filter(Course.course_code.ilike(code))

    # create list of dict of course information
    course_codes = []
    for course in courses:
        id = course.id
        author = str(course.user_netid)
        staff_cert = False if user.user_type == "student" else True
        course_code = course.course_code
        course_name = course.course_name
        last_updated = course.last_updated.strftime("%m/%d/%y %I:%M%p")
        course_codes.append({"course_code": course_code,
                             "course_name": course_name,
                             "author": author,
                             "staff_cert": staff_cert,
                             "id": id,
                             "last_updated": last_updated})

    return render_template("searchpubliccourses.html",
                           courses=course_codes)

@bp.route("/publicassignments", methods=["GET", "POST"])
@login_required
def public_assignments():
    try:
        id = request.args.get("courseid")

        course = Course.query.get(id)
        assignments = course.assignments

        assignment_data = []
        course_code = course.course_code
        author = course.user_netid
        for a in assignments:
            due = a.due_date.strftime("%b %d, %Y %I:%M%p")
            assignment_data.append({
                                    "id": a.id,
                                    "title": a.title,
                                    "due_date": due,
                                    "course_code": course.course_code})
        return render_template("publicassignments.html",
                               author=author,
                               assignments=assignment_data, 
                               course_code=course_code,
                               id=id)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return render_template("error.html", message=ex)

@bp.route("/importcourses", methods=["GET", "POST"])
@login_required
def import_courses():
    try:
        course_ids = request.form.get("selected_courses")
        # when nothing is selected to be imported this is where we catch
        if course_ids == "":
            return redirect(url_for(".public_courses"))

        course_list = course_ids.split(",")
        netid = session["netid"]
        user = User.query.get(netid)

        for id in course_list:
            course = Course.query.get(id)
            course_code = course.course_code
            course_name = course.course_name
            assignments = course.assignments

            new_id = generate_course_id()
            new_course = Course(id=new_id, course_code=course_code,
                                course_name=course_name, color="#FFC78F",
                                user_netid=netid)
            user.courses.append(new_course)
            db.session.add(new_course)

            # commit so new_course exists before assignments are added to it
            db.session.commit()

            assignments = list(course.assignments)
            for a in assignments:
                assignment_id = generate_assignment_id()
                import_assignment = Assignment(id=assignment_id,
                                               title=a.title,
                                               due_date=a.due_date,
                                               status=0,
                                               course_id=new_id)
                db.session.add(import_assignment)

        db.session.commit()
        return redirect(url_for(".hub"))
    except Exception as ex:
            print(ex, file=sys.stderr)
            return render_template("error.html", message=ex)
