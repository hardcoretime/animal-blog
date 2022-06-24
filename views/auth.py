from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user

from models import User, db, db_add_obj

auth_app = Blueprint('auth_app', __name__)


@auth_app.route("/login/", endpoint='login')
def login():
    return render_template('auth/login.html')


@auth_app.route('/login/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth_app.login'))

    login_user(user, remember=True)
    return redirect(url_for('profile'))


@auth_app.route("/signup/", endpoint='signup')
def signup():
    return render_template('auth/signup.html')


@auth_app.route("/signup/", methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth_app.signup'))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256')
    )
    db_add_obj(db, new_user)

    return redirect(url_for('auth_app.login'))


@auth_app.route("/logout/", endpoint='logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts_app.list'))
