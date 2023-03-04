from flask import Blueprint, redirect, url_for, flash, request, render_template, current_app
from itsdangerous import URLSafeTimedSerializer as URLSerializer
from itsdangerous import SignatureExpired, BadTimeSignature
from flask_login import *
from datetime import timedelta, date
from Attendive import db, bcrypt
from Attendive.student.utils import *
from Attendive.models import *
import os

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
        semester = request.form.get('semester')
        terms = request.form.get('terms')
        if terms == 'on':
            if not User.query.filter_by(email=email).first() and not User.query.filter_by(mobile_number=mobile_number).first() or not User.query.filter_by(enrollment=enrol).first():
                if password == cpassword:
                    s = URLSerializer(current_app.config['SECRET_KEY'])
                    token = s.dumps({"email": email, "fname": fname, "lname": lname, "mobile_number": mobile_number, "password": password, "section": section, "enrol": enrol, "semester": semester}, salt="send-email-confirmation")
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
                    section=data["section"], semester=data["semester"], date=datetime.now(tz))
        db.session.add(user)
        role = Role.query.filter_by(name='student').first()
        user.roles.append(role)
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
        return redirect(url_for('student.attendance'))
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "success")
        return redirect(url_for('student.login'))
    return render_template('student/forgot_password.html')

@student.route('/reset_password/<token>/', methods=['GET', 'POST'])
def reset_token(token):
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
    if not current_user.is_approved:
        flash("Contact your HOD for confirmation.", "info")
        return redirect(url_for('student.settings'))
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        return redirect(url_for('faculty.attendance'))
    if not current_user.files_uploaded:
        return redirect(url_for('student.settings'))
    attendances = Attendance.query.filter_by(user_id=current_user.id).all()
    return render_template('student/attendance.html', attendances=attendances)

@student.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        return redirect(url_for('faculty.attendance'))
    if request.method == 'POST':
        if request.args.get('form') == 'change_password':
            current_password = request.form.get('current_password')
            password = request.form.get('password')
            cpassword = request.form.get('cpassword')
            if password == cpassword:
                if bcrypt.check_password_hash(current_user.password, current_password):
                    current_user.password = bcrypt.generate_password_hash(password)
                    db.session.commit()
                    flash("Your password has been changed!", "success")
                    return redirect(url_for('student.settings'))
                else:
                    flash("Current password does not match.", "danger")
                    return redirect(url_for('student.settings'))
            else:
                flash("Password and confirm password must be same.", "danger")
                return redirect(url_for('student.settings'))
        if request.args.get('form') == 'add_face':
            if request.files:
                front = save_picture(current_user.id, request.files.get('frontface'))
                if not front:
                    flash("Allowed files are png, jpg, jpeg.", "danger")
                    return redirect(url_for('student.settings'))
                current_user.front_face = front
                print(front)
                
                if front:
                    current_user.files_uploaded = True
                    db.session.commit()
                db.session.commit()
                flash("Image saved for attendance.", "success")
                return redirect(url_for('student.settings'))
    return render_template('student/settings.html')

@student.route('/apply_leave/', methods=['GET', 'POST'])
@login_required
def apply_leave():
    if not current_user.is_approved:
        flash("Contact your HOD for confirmation.", "info")
        return redirect(url_for('student.settings'))
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        return redirect(url_for('faculty.attendance'))
    if not current_user.files_uploaded:
        return redirect(url_for('student.settings'))
    if current_user.leaves_left == 0:
        flash("Your allocated leaves are 0.", "danger")
        return redirect(url_for('student.attendance'))
    if request.method == 'POST':
        if current_user.leaves_left != 0:
            application_type = request.form.get('application_type')
            apply_date = request.form.get('apply_date')
            leavefrom = request.form.get('leavefrom')
            leavetill = request.form.get('leavetill')
            num_days = request.form.get('num_days')
            reason = request.form.get('reason')
            f_yr, f_mon, f_dy = map(int, apply_date.split(('-')))
            apply_date = date(f_yr, f_mon, f_dy)
            f_yr, f_mon, f_dy = map(int, leavefrom.split(('-')))
            leavefrom = date(f_yr, f_mon, f_dy)
            t_yr, t_mon, t_dy = map(int, leavetill.split(('-')))
            leavetill = date(t_yr, t_mon, t_dy)
            appli = Application(application_type=application_type, apply_date=apply_date, leave_from=leavefrom, leave_till=leavetill, total_days_left=num_days, total_days=num_days, reason=reason, status='REQUESTED', user_id=current_user.id)
            db.session.add(appli)
            db.session.commit()
            flash("Applied Successfully!", "success")
            return redirect(url_for('student.application'))
        else:
            flash("Allocated leaves exceed.", "danger")
            return redirect(url_for('student.apply_leave'))
    return render_template('student/apply_leave.html')

@student.route('/application/')
@login_required
def application():
    if not current_user.is_approved:
        flash("Contact your HOD for confirmation.", "info")
        return redirect(url_for('student.settings'))
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' not in user_roles:
        return redirect(url_for('faculty.attendance'))
    if not current_user.files_uploaded:
        return redirect(url_for('student.settings'))
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('student/applications.html', applications=applications)
