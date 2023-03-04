from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from Attendive.config import Config
from flask_bcrypt import Bcrypt
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'student.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from Attendive.main.views import main
    from Attendive.student.views import student
    from Attendive.faculty.views import faculty
    from Attendive.admin.views import admin
    app.register_blueprint(main)
    app.register_blueprint(student)
    app.register_blueprint(faculty)
    app.register_blueprint(admin)

    return app
