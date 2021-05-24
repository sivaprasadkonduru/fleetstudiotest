from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/fleetstudiodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserModel(db.Model):

    __tablename__ = 'usertable'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(6), unique=True)
    phone_no = db.column(db.Integer, unique=True)