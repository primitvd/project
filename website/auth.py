from flask import Blueprint, render_template, request, flash
from .models import *
from . import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/managerlogin', methods=['GET','POST'])
def manlogin():
    if not login.query.all():
        manager = login(user_id="manager", password="manager")
        admin = login(user_id="admin", password="admin")
        db.session.add(manager)
        db.session.add(admin)
        db.session.commit()
    data = request.form.get("pass1")
    if request.method == 'POST':
        data1 = login.query.all()
        for data2 in data1:
            print(data2.password)
        print(data1)
        flash(data, category='success')
    login1 = login.query.all()
    return render_template("managerlogin.html", login2=login1)

@auth.route('/adminlogin', methods=['GET','POST'])
def adlogin():
    pass1 = request.form.get("pass1")
    pass12 = request.form.get("pass12")
    n = 0
    if request.method == 'POST':
        # for user in db.session.query(login.user_id):
        login1 = login.query.all()
        for user in login1:
            print(user)
            print(pass12)
            if pass12 == user.user_id:
                n = 1
                user1 = login.query.filter_by(user_id='pass12').first()
                print(user1)
                # user1["password"] = pass1
                db.session.commit()
                flash('Account already exists',category=False)
        if n == 0:
            new_user = login(user_id = pass12, password = pass1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created',category=True)
    return render_template("adminlogin.html")


@auth.route('/logout')
def logout():
    return render_template("home.html")