from flask import Blueprint, make_response, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user
from .models import *
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/managerlogin', methods=['GET','POST'])
def manlogin():
    if request.method == 'POST':
        userid = "manager"
        password = request.form.get('password')

        user = logins.query.filter_by(user_id=userid).first()
        
        if user:
            if(check_password_hash(user.password, password)):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template("managerlogin.html", user=current_user)

@auth.route('/adminlogin', methods=['GET','POST'])
def adlogin():
    if request.method == 'POST':
        userid = "admin"
        password = request.form.get('password')

        user = logins.query.filter_by(user_id=userid).first()
        
        if user:
            if(check_password_hash(user.password, password)):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template("adminlogin.html",  user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('user_id')
        password = request.form.get('password')
        user = logins.query.filter_by(user_id=userid).first()
        
        if user:
            if(check_password_hash(user.password, password)):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                respo = make_response(url_for('views.home'))
                # respo.set_cookie('username')
                return respo
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    resp = make_response(render_template("login.html", user=current_user))
    # resp.set_cookie("username")
    return resp


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/changepassword', methods=['GET','POST'])
@login_required
def changepassword():
    if request.method == 'POST':
        userid = request.form.get('user_id')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        user = logins.query.filter_by(user_id=userid).first()

        if user:
            if(password == password1):
                user.password = generate_password_hash(password, method='sha256')
                flash('Password changed successfully!', category='success')
                login_user(user, remember=True)
                db.session.commit()
            else:
                flash('Passwords do not match, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    
    return render_template("changepassword.html", user=current_user)