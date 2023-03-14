import os
from flask import Flask, render_template, request, redirect, url_for
from psycopg2 import connect


app = Flask(__name__)

hostname = "dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com"
connect_db = connect(database="tigerfocus_4gqq", user="admin",
        password=os.environ["DB_PASSWORD"], host=hostname, port="5432")

@app.route("/")
def index():
    conn = connect_db    
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
    conn.close()

    return render_template("index.html", data=data)

@app.route("/adduser")
def add_user():
    return render_template("adduser.html")

@app.route("/createduser")
def created_user():
    id = request.args.get("userid")
    first = request.args.get("first")
    last = request.args.get("last")

    try:
        conn = connect_db
        with conn.cursor() as cur:
            cur.execute("SELECT NOW()")
            now = cur.fetchone()
            query = "INSERT INTO "
            query += "users(user_id, first_name, last_name, last_login)"
            query += f"VALUES ({id}, {first}, {last}, {now})"

            cur.execute(query)
        conn.close()
        
        return render_template("success.html", name=first)
    except Exception:
        return render_template("error.html")

if __name__ == "__main__":
    app.run()
