import os
from flask import Flask, render_template, request, redirect, url_for
from psycopg2 import connect

app = Flask(__name__, template_folder="./templates")

hostname = os.environ.get("DB_HOST")
connect_db = connect(
    database="tigerfocus_4gqq",
    user="admin",
    password="LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6",
    host=hostname,
    port="5432")

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        with connect_db as conn:
            print("Connecting to PostgreSQL database")
            with conn.cursor() as cur:
                print("Creating cursor")
                cur.execute("SELECT * FROM users")
                data = cur.fetchall()
            print("Cursor closed")
        print("Database connection closed")
        return render_template("index.html", data=data)
    except Exception as ex:
        print('{} - connection will be reset'.format(ex))
        # Close old connection 
        if conn:
            if cursor:
                cursor.close()
            conn.close()
        conn = None
        cursor = None
        
        # Reconnect 
        conn = connect_db
        cursor = conn.cursor()

@app.route("/hub")
def hub():
    return render_template("hub.html")

@app.route("/adduser")
def add_user():
    return render_template("adduser.html")

@app.route("/createduser", methods=["GET", "POST"])
def created_user():
    id = request.form.get("userid")
    first = request.form.get("first")
    last = request.form.get("last")

    try:
        with connect_db as conn:
            print("Connecting to PostgreSQL database")
            with conn.cursor() as cur:
                print("Creating cursor")
                query = "INSERT INTO users(user_id, first_name, last_name)"
                query += "VALUES(%s, %s, %s)"
                cur.execute(query, (id, first, last))
            print("Cursor closed")
        print("Database connection closed")
        return redirect(url_for("index"), code=307)
    except Exception as ex:
        print(ex)
        return render_template("error.html", link=(url_for('index')))

if __name__ == "__main__":
    app.run()
