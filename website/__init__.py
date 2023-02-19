from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

DB = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'project'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB}'
    db.init_app(app)

    from .views import views
    from .auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models
    from .models import logins

    with app.app_context():
        db.create_all()
        if not models.logins.query.all():
            manager = models.logins(user_id="manager", password=generate_password_hash("manager", method='sha256'))
            admin = models.logins(user_id="admin", password=generate_password_hash("admin", method='sha256'))
            db.session.add(manager)
            db.session.add(admin)
            db.session.commit()
        print('Created Database')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return logins.query.get(user_id)

    return app
