"""
BEFORE RUNNING:
    run the line below in terminal
    export DB_HOST=dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com
"""

import psycopg2, os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
course_counter = 100000

connect_db = psycopg2.connect(
    database="tigerfocus_4gqq",
    user="admin",
    password="LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6",
    host=os.environ["DB_HOST"],
    port="5432")

@app.route("/", methods=["GET"])
def index():
    try:
        with connect_db.cursor() as cur:
            cur.execute("SELECT * FROM user_info")
            data = cur.fetchall()
        return render_template("index.html", data=data)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/adduser")
def add_user():
    return render_template("register.html")

@app.route("/createduser", methods=["GET", "POST"])
def created_user():
    id = request.form.get("userid")
    first = request.form.get("first")
    last = request.form.get("last")

    try:
        with connect_db.cursor() as cur:
            query = "INSERT INTO users(user_id, first_name, last_name)"
            query += "VALUES(%s, %s, %s)"
            cur.execute(query, (id, first, last))
        return redirect(url_for("index"))
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/selectuser", methods=["GET", "POST"])
def select_user():
    try:
        with connect_db.cursor() as cur:
            query = "SELECT PUID FROM user_info"
            cur.execute(query)
            ids = cur.fetchall()
        return render_template("selectuser.html", userids=ids)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/viewcourses")
def view_courses():
    userid = request.form.get("userid")
    try:
        course_codes = []
        with connect_db.cursor() as cur:
            query = "SELECT courseids FROM user_info WHERE PUID=%s"
            cur.execute(query, (userid,))
            courseids = cur.fetchall()
            for id in courseids:
                query = "SELECT course_code FROM courses WHERE courseid=%s"
                cur.execute(query, (id,))
                coursecode = cur.fetchone()
                course_codes.append(coursecode)
        return render_template("courses.html", userid=userid,
                               codes=course_codes)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

    return render_template("viewcourses.html")

@app.route("/addcourse", methods=["GET", "POST"])
def add_course():
    try:
        userid = request.form.get("userid")
        return render_template("addcourse.html", userid=userid)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/createdcourse", methods=["GET", "POST"])
def created_course():
    try:
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        userid = request.form.get("userid")
        with connect_db.cursor() as cur:
            query = "UPDATE user_info SET courseids = "
            query += "array_append(courseids, %s) WHERE PUID=%s"
            cur.execute(query, (course_counter, userid))
            query = "INSERT INTO courses(courseid, course_code, "
            query += "course_name, course_color) VALUES"
            query += "(%s, %s, %s, %s)"
            cur.execute(query, course_counter, course_code,
                        course_name, course_color)
        course_counter += 1
        return redirect(url_for("viewcourses"))
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/hub")
def hub():
    return render_template("hub.html")

@app.route("/timer")
def timer():
    return render_template("timer.html")

if __name__ == "__main__":
    app.run(port=5001)
