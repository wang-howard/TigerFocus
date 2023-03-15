import os
from flask import Flask, render_template, request, redirect, url_for
from psycopg2 import connect


app = Flask(__name__)

hostname = "dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com"
connect_db = connect(database="tigerfocus_4gqq", user="admin",
            password="LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6", host=hostname,
            port="5432")

@app.route("/")
def index():
    with connect_db as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()

    return render_template("index.html", data=data)

@app.route("/hub")
def hub():
    return render_template("hub.html")

@app.route("/adduser")
def add_user():
    return render_template("adduser.html")

@app.route("/createduser", methods=["GET", "POST"])
def created_user():
    id = request.args.get("userid")
    first = request.args.get("first")
    last = request.args.get("last")

    try:
        with connect_db as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT NOW()")
                now = cur.fetchone()[0]
                query = "INSERT INTO "
                query += "users(user_id, first_name, last_name, last_login)"
                query += "VALUES (%s, %s, %s, %s)"
                print("BLAH FIRST")
                cur.execute(query, (id, first, last, now))
                print("BLAH")

        return render_template("success.html", name=first)
    except Exception as ex:
        print(ex)
        return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)
