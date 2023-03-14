from flask import Flask, render_template, request, redirect, url_for
from psycopg2 import connect


app = Flask(__name__)



@app.route("/")
def index():
    conn = connect(database="tigerfocus_4gqq", user="admin",
            password="LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6",
            host="dpg-cg57dujhp8u9l205a1jg-a.ohio-postgres.render.com",
            port="5432")
            
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
    
    conn.close()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
