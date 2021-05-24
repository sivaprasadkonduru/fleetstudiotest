from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import re

from models import UserModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/fleetstudiodb'
db = SQLAlchemy(app)


@app.route('/login/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        # If account exists in accounts table in out database
        user = UserModel.query.filter_by(username=username).first()
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg='')


@app.route('/login/logout')
def logout():
    #this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/login/signup', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_no = request.form['phone_no']
        user = UserModel.query.filter_by(username=username).first()
        # If account exists show error and validation checks
        if user:
            msg = 'User already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            new_user = UserModel(username=username, email=email, password=password, phone_no=phone_no)
            # saving user object into data base with hashed password
            db.session.add(new_user)
            db.session.commit()
            msg = 'You have successfully registered a user: {}'.format(username)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
