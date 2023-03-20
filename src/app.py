import psycopg2, os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

hostname = "dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com"
connect_db = psycopg2.connect(
    database="tigerfocus_4gqq",
    user="admin",
    password="LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6",
    host=hostname,
    port="5432")

@app.route("/", methods=["GET"])
def index():
    try:
        with connect_db as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users")
                data = cur.fetchall()
        return render_template("index.html", data=data)
    except Exception as ex:
        print(ex)
        return render_template("error.html")

@app.route("/hub")
def hub():
    return render_template("hub.html")

@app.route("/timer")
def timer():
    return render_template("timer.html")

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
                query = "INSERT INTO users(user_id, first_name, last_name)"
                query += "VALUES(%s, %s, %s)"
                cur.execute(query, (id, first, last))
        return redirect(url_for("index"))
    except Exception as ex:
        print(ex)
        return render_template("error.html")

if __name__ == "__main__":
    app.run(port=5001)
