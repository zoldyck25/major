from flask import Blueprint, redirect, url_for, flash, request, render_template, current_app, Response
from itsdangerous import URLSafeTimedSerializer as URLSerializer
from itsdangerous import SignatureExpired, BadTimeSignature
from flask_login import *
from datetime import datetime, timedelta, date
from Attendive import db, bcrypt
from Attendive.faculty.utils import *
from Attendive.models import *

faculty = Blueprint('faculty', __name__)


@faculty.route('/faculty/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('faculty.attendance'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember_me')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Faculty Not Found.", "danger")
            return redirect(url_for('faculty.register'))
        if bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True if remember=='on' else False, duration=timedelta(days=3))
            next_page = request.args.get('next')
            flash("Faculty logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for('faculty.attendance'))
        else:
            flash("Please check you password. Password don't match!", "danger")
            return redirect(url_for('faculty.login'))
    return render_template('faculty/login.html')

@faculty.route('/faculty/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('faculty.attendance'))
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        terms = request.form.get('terms')
        if terms == 'on':
            if not User.query.filter_by(email=email).first() and not User.query.filter_by(mobile_number=mobile_number).first():
                if password == cpassword:
                    s = URLSerializer(current_app.config['SECRET_KEY'])
                    token = s.dumps({"email": email, "fname": fname, "lname": lname, "mobile_number": mobile_number, "password": password}, salt="send-email-confirmation")
                    send_faculty_confirm_email(email=email, token=token)
                    flash(f"An confirmation email has been sent to you on {email}!", "success")
                    return redirect(url_for('faculty.login'))
                else:
                    flash(f"Password does not match with confirm pasword!", "danger")
                    return redirect(url_for('faculty.register'))
            else:
                flash(f"An account with {email} or {mobile_number} is already exist!", "danger")
                return redirect(url_for('faculty.login'))
    return render_template('faculty/register.html')

@faculty.route('/faculty/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('faculty.login'))

#student------ Confirm Registration ------ #
@faculty.route('/faculty/confirm_email/<token>/')
def confirm_email(token):
    s = URLSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt="send-email-confirmation", max_age=600)
        if User.query.filter_by(email=data['email']).first():
            flash("You have an account! Please login to continue.", "success")
            return redirect(url_for('faculty.login'))
        user = User(fname=data["fname"], email=data["email"], lname=data["lname"], mobile_number=data["mobile_number"],
                    password=bcrypt.generate_password_hash(data["password"]).decode('utf-8'), 
                    date=datetime.now(tz), files_uploaded=True, is_approved=True)
        db.session.add(user)
        role = Role.query.filter_by(name='faculty').first()
        user.roles.append(role)
        db.session.commit()
        login_user(user, remember=True, duration=timedelta(hours=1))
        flash("Your account has been created successfully!", "success")
        return redirect(url_for('faculty.attendance'))
    except (SignatureExpired, BadTimeSignature):
        flash("That is an invalid or expired token", "danger")
        return redirect(url_for('faculty.login'))

@faculty.route('/faculty/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('faculty.attendance'))
    if request.method == "POST":
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        send_faculty_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "success")
        return redirect(url_for('faculty.login'))
    return render_template('faculty/forgot_password.html')

@faculty.route('/faculty/reset_password/<token>/', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "danger")
        return redirect(url_for('faculty.forgot_password'))
    if request.method == "POST":
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if password == cpassword:
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.session.commit()
            flash("Your password has been updated! You are now able to login", "success")
            return redirect(url_for('faculty.login'))
        else:
            flash(f"Password does not match with confirm password!", "danger")
            return redirect(url_for('faculty.login'))
    return render_template('faculty/reset_token.html', token=token)

@faculty.route('/faculty/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' in user_roles:
        return redirect(url_for('student.attendance'))
    if 'faculty' not in user_roles:
        return redirect(url_for('main.home'))
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
                    return redirect(url_for('faculty.settings'))
                else:
                    flash("Current password does not match.", "danger")
                    return redirect(url_for('faculty.settings'))
            else:
                flash("Password and confirm password must be same.", "danger")
                return redirect(url_for('faculty.settings'))
    return render_template('faculty/settings.html')

@faculty.route('/faculty/mark_attendance/', methods=['GET', 'POST'])
@login_required
def attendance():
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' in user_roles:
        return redirect(url_for('student.attendance'))
    if 'faculty' not in user_roles:
        return redirect(url_for('main.home'))
    subjects = list(current_user.subjects)
    if request.method=='POST':
        attendance_date = request.form.get('attendance_date')
        period_number = request.form.get('period_number')
        semester = request.form.get('semester')
        subject = request.form.get('subjects')
        section = request.form.get('section')
        unit_number = request.form.get('unit_number')
        topic = request.form.get('topic')
        total_attendance = request.form.get('total_attendance')
        return redirect(url_for('faculty.submit_attendance', attendance_date=attendance_date, period_number=period_number, semester=semester, subject=subject, section=section, unit_number=unit_number, topic=topic, total_attendance=total_attendance))
    return render_template('faculty/mark_attendance.html', subjects=subjects)

@faculty.route('/faculty/submit_attendance/<attendance_date>/<period_number>/<semester>/<subject>/<section>/<unit_number>/<topic>/<total_attendance>/')
@login_required
def submit_attendance(attendance_date, period_number, semester, subject, section, unit_number, topic, total_attendance):
    users = User.query.filter_by(section=section).filter_by(semester=int(semester)).all()
    for user in users:
        f_yr, f_mon, f_dy = map(int, attendance_date.split(('-')))
        attendance_date_new = date(f_yr, f_mon, f_dy)
        if not Attendance.query.filter_by(user_id=user.id).filter_by(date=attendance_date).filter_by(subject=subject).filter_by(topic=topic).first():
            for _ in range(int(total_attendance)):
                att = Attendance(date=attendance_date_new, section=section, period_number=period_number, unit_number=unit_number, subject=subject, status='NA', topic=topic, user_id=user.id)
                db.session.add(att)
                db.session.commit()
    return render_template('faculty/submit_attendance.html', attendance_date=attendance_date, period_number=period_number, semester=semester, subject=subject, section=section, unit_number=unit_number, topic=topic, total_attendance=total_attendance)


@faculty.route('/video_feed/<semester>/<subject>/<section>/')
@login_required
def video_feed(semester, subject, section):
    user_roles = [role.name for role in list(current_user.roles)]
    if 'student' in user_roles:
        return redirect(url_for('student.attendance'))
    if 'faculty' not in user_roles:
        return redirect(url_for('main.home'))

    # Import Video from file
    from Attendive.faculty.camera import Video
    role = Role.query.filter_by(name='student').first()
    users = list()
    for user in role.user:
        if user.semester == int(semester) and user.section == section:
            users.append(user)
    return Response(Video.gen_frames(users, current_app.root_path, subject, section), mimetype='multipart/x-mixed-replace; boundary=frame')


@faculty.route('/faculty/marking_attendance/<id>/<subject>/<section>/<token>/', methods=['GET', 'POST'])
def marking_attendance(id, subject, section, token):
    if token == 'dd85fe3ab7ec25ea4190':
        user = User.query.filter_by(id=id).first()
        for attendance in user.attendances:
            print(attendance)
            if attendance.status == 'NA' and attendance.section == section and attendance.subject == subject:
                attendance.status = 'P'
                db.session.commit()
        return str(user.id)
    return '0'

