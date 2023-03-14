from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.configapp.config['SQLALCHEMY_DATABASE_URI'] = \
    "postgresql://admin:LbAGfF63trlyTzUF8ZgKvxO01k1pmsi6@" + \
        "dpg-cg57dujhp8u9l205a1jg-a/tigerfocus_4ggq"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = '098098'

db = SQLAlchemy(app)


