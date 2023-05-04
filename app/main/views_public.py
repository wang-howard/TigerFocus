import sys, random
from datetime import date
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
from . import bp
from .. import db
from ..models import User, Course, Assignment, Public_Course, Public_Assignment

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
    title = request.args.get('title')
    code = request.args.get('code')
    title = "%{}%".format(title)
    code = "%{}%".format(code)
    courses = Public_Course.query\
                .filter(Public_Course.course_name.ilike(title))\
                .filter(Public_Course.course_code.ilike(code))

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

    return render_template("searchpubliccourses.html",
                           courses=course_codes)

@bp.route("/publicassignments", methods=["GET", "POST"])
@login_required
def public_assignments():
    try:
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
        course_ids = request.form.get('selected_courses')
        # when nothing is selected to be imported this is where we catch
        if course_ids == '':
            return redirect(url_for(".public_courses"))

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
