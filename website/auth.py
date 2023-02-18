from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import current_user, login_required, login_user, logout_user
from .models import *
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/managerlogin', methods=['GET','POST'])
def manlogin():
    data = request.form.get("pass1")
    if request.method == 'POST':
        data1 = logins.query.all()
        for data2 in data1:
            print(data2.password)
        print(data1)
        flash(data, category='success')
    login1 = logins.query.all()
    return render_template("managerlogin.html", login2=login1, user=current_user)

@auth.route('/adminlogin', methods=['GET','POST'])
def adlogin():
    pass1 = request.form.get("pass1")
    pass12 = request.form.get("pass12")
    n = 0
    if request.method == 'POST':
        # for user in db.session.query(login.user_id):
        login1 = logins.query.all()
        for user in login1:
            print(user)
            print(pass12)
            if pass12 == user.user_id:
                n = 1
                user1 = logins.query.filter_by(user_id='pass12').first()
                print(user1)
                # user1["password"] = pass1
                db.session.commit()
                flash('Account already exists',category=False)
        if n == 0:
            new_user = logins(user_id = pass12, password = pass1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created',category=True)
    return render_template("adminlogin.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('user_id')
        password = request.form.get('password')

        user = logins.query.filter_by(user_id=userid).first()
        
        if user:
            if(user.password == password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)


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
                user.password = password
                flash('Password changed successfully!', category='success')
                login_user(user, remember=True)
                db.session.commit()
            else:
                flash('Passwords do not match, try again.', category='error')
        else:
            flash('User does not exist.', category='error')


    return render_template("changepassword.html", user=current_user)