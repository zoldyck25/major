from flask import Blueprint, redirect, url_for, flash, request, render_template, current_app
from itsdangerous import URLSafeTimedSerializer as URLSerializer
from itsdangerous import SignatureExpired, BadTimeSignature
from flask_login import *
from datetime import timedelta
from Attendive import db, bcrypt
from Attendive.student.utils import send_confirm_email, send_reset_email
from Attendive.models import *

student = Blueprint('student', __name__)

@student.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student.attendance'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember_me')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User Not Found.", "danger")
            return redirect(url_for('student.register'))
        if bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True if remember=='on' else False, duration=timedelta(days=3))
            next_page = request.args.get('next')
            flash("User logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for('student.attendance'))
        else:
            flash("Please check you password. Password don't match!", "danger")
            return redirect(url_for('student.login'))
    return render_template('student/login.html')

@student.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.attendance'))
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        section = request.form.get('section')
        enrol = request.form.get('enrol')
        terms = request.form.get('terms')
        if terms == 'on':
            if not User.query.filter_by(email=email).first() and not User.query.filter_by(mobile_number=mobile_number).first() or not User.query.filter_by(enrollment=enrol).first():
                if password == cpassword:
                    s = URLSerializer(current_app.config['SECRET_KEY'])
                    token = s.dumps({"email": email, "fname": fname, "lname": lname, "mobile_number": mobile_number, "password": password, "section": section, "enrol": enrol}, salt="send-email-confirmation")
                    send_confirm_email(email=email, token=token)
                    flash(f"An confirmation email has been sent to you on {email}!", "success")
                    return redirect(url_for('student.login'))
                else:
                    flash(f"Password does not match with confirm pasword!", "danger")
                    return redirect(url_for('student.register'))
            else:
                flash(f"An account with {email} or {mobile_number} is already exist!", "danger")
                return redirect(url_for('student.login'))
    return render_template('student/register.html')


@student.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('student.login'))

#student------ Confirm Registration ------ #
@student.route('/confirm_email/<token>/')
def confirm_email(token):
    s = URLSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt="send-email-confirmation", max_age=600)
        if User.query.filter_by(email=data['email']).first():
            flash("You have an account! Please login to continue.", "success")
            return redirect(url_for('student.login'))
        user = User(fname=data["fname"], email=data["email"], lname=data["lname"], mobile_number=data["mobile_number"],
                    password=bcrypt.generate_password_hash(data["password"]).decode('utf-8'), enrollment=data["enrol"], 
                    section=data["section"], date=datetime.now(tz))
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True, duration=timedelta(hours=1))
        flash("Your account has been created successfully!", "success")
        return redirect(url_for('student.attendance'))
    except (SignatureExpired, BadTimeSignature):
        flash("That is an invalid or expired token", "danger")
        return redirect(url_for('student.login'))


@student.route('/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('student.settings'))
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "success")
        return redirect(url_for('student.login'))
    return render_template('student/forgot_password.html')

@student.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('student.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "danger")
        return redirect(url_for('student.forgot_password'))
    if request.method == "POST":
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if password == cpassword:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            flash("Your password has been updated! You are now able to login", "success")
            return redirect(url_for('student.login'))
        else:
            flash(f"Password does not match with confirm password!", "danger")
            return redirect(url_for('student.login'))
    return render_template('student/reset_token.html', token=token)


@student.route('/attendance/', methods=['GET', 'POST'])
@login_required
def attendance():
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        flash("You are not allowed to visit student dashboard", "danger")
        return redirect(url_for('main.home'))
    if not current_user.files_uploaded:
        return redirect(url_for('student.settings'))
    return render_template('student/attendance.html')

@student.route('/settings/')
@login_required
def settings():
    return render_template('student/settings.html')

@student.route('/apply_leave/')
@login_required
def apply_leave():
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        flash("You are not allowed to visit student dashboard", "danger")
        return redirect(url_for('main.home'))
    if not current_user.files_uploaded:
        return redirect(url_for('student.settings'))
    return render_template('student/apply_leave.html')

@student.route('/application/')
@login_required
def application():
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        flash("You are not allowed to visit student dashboard", "danger")
        return redirect(url_for('main.home'))
    if not current_user.files_uploaded:
        return redirect(url_for('student.settings'))
    return render_template('student/applications.html')
