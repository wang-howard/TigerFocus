import sys, random
from datetime import date
from flask import render_template, redirect, url_for
from flask import session, request
from flask_login import login_required
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

        return redirect(url_for(".instructor_assignments", courseid=course_id))
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