from flask import current_app
from Attendive import db, login_manager
from datetime import datetime
import pytz
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

tz = pytz.timezone("Asia/Calcutta")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_role = db.Table('user_role',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

user_subject = db.Table('user_subject',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(128))
    lname = db.Column(db.String(128))
    email = db.Column(db.String(140), unique=True, nullable=False)
    mobile_number = db.Column(db.String(11), unique=True, nullable=False)
    section = db.Column(db.String(255))
    semester = db.Column(db.Integer)
    enrollment = db.Column(db.String(128))
    password = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(tz))
    leaves_left = db.Column(db.Integer, default=10)
    files_uploaded = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role', backref='user', secondary=user_role, lazy='dynamic')
    subjects = db.relationship('Subject', backref='user', secondary=user_subject, lazy='dynamic')

    # Student
    front_face = db.Column(db.String(200)) # Front

    # Student - Relations
    applications = db.relationship('Application', backref='user', lazy='dynamic')
    attendances = db.relationship('Attendance', backref='user', lazy='dynamic')

    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    section = db.Column(db.String(100), nullable=False)
    period_number = db.Column(db.Integer, nullable=False)
    unit_number = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    topic = db.Column(db.Text(), nullable=False)
    marked_attendance = db.Column(db.DateTime(), default=datetime.now(tz))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"({self.subject} - {self.date} - {self.status})"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_type = db.Column(db.String(100), nullable=False)
    apply_date = db.Column(db.Date(), nullable=False)
    leave_from = db.Column(db.Date(), nullable=False)
    leave_till = db.Column(db.Date(), nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    total_days_left = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.Text(), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

class Faculty_Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('user.id'))
