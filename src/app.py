"""
BEFORE RUNNING:
    run the lines below in terminal
    export DB_HOST=dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com
    export SEC_KEY=tigerFocus098098
"""

import psycopg2, os, uuid, random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SEC_KEY")
bootstrap = Bootstrap(app)

connect_db = psycopg2.connect(
    database="tigerfocus_4gqq",
    user="admin",
    password="LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6",
    host=os.getenv("DB_HOST"),
    port="5432")

class SelectIDForm(FlaskForm):
    userid = SelectField("Select PUID", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET"])
def index():
    try:
        with connect_db as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM user_info ORDER BY last_name ASC")
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
        with connect_db as conn:
            with conn.cursor() as cur:
                query = "INSERT INTO user_info(puid, first_name, last_name)"
                query += "VALUES(%s, %s, %s)"
                cur.execute(query, (id, first, last))
        return redirect(url_for("index"))
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/selectuser", methods=["GET", "POST"])
def select_user():
    try:
        with connect_db as conn:
            with conn.cursor() as cur:
                query = "SELECT puid FROM user_info ORDER BY puid ASC"
                cur.execute(query)
                ids = cur.fetchall()
        users = []
        for id in ids:
            users.append(id[0])
        form = SelectIDForm()
        form.userid.choices = users
        if form.validate_on_submit():
            session["userid"] = form.userid.data
            return redirect(url_for("view_courses"))
        return render_template("selectuser.html", form=form)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/viewcourses", methods=["GET", "POST"])
def view_courses():
    userid = session["userid"]
    try:
        course_codes = []
        with connect_db as conn:
            with conn.cursor() as cur:
                query = "SELECT courseids FROM user_info WHERE PUID=%s"
                cur.execute(query, (userid,))
                courseids = cur.fetchone()
                if courseids and courseids[0]:
                    for id in courseids[0]:
                        query = "SELECT course_code FROM course WHERE courseid=%s"
                        cur.execute(query, (id,))
                        coursecode = cur.fetchone()
                        course_codes.append(coursecode[0])
                else:
                    course_codes = []
        return render_template("courses.html", userid=userid,
                               codes=course_codes)
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/addcourse", methods=["GET", "POST"])
def add_course():
    try:
        return render_template("addcourse.html")
    except Exception as ex:
        print(ex)
        return render_template("error.html", message=ex)

@app.route("/createdcourse", methods=["GET", "POST"])
def created_course():
    global course_counter
    try:
        course_code = request.form.get("course_code")
        course_name = request.form.get("course_name")
        course_color = request.form.get("color")
        userid = session["userid"]
        courseid = str(random.randint(0, 999999)).zfill(6)
        with connect_db as conn:
            with conn.cursor() as cur:
                while True:
                    query = "SELECT courseid FROM course WHERE courseid=%s"
                    cur.execute(query, (courseid,))
                    result = cur.fetchone()
                    if not result:
                        break
                    else:
                        courseid = str(random.randint(0, 999999)).zfill(6)
                query = "UPDATE user_info SET courseids = "
                query += "array_append(courseids, %s) WHERE PUID=%s"
                cur.execute(query, (courseid, userid))
                query = "INSERT INTO course(courseid, course_code, "
                query += "course_name, course_color) VALUES"
                query += "(%s, %s, %s, %s)"
                cur.execute(query, (courseid, course_code,
                            course_name, course_color))
        return redirect(url_for("view_courses"))
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
    app.run(port=5555, debug=True)