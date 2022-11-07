from flask import Blueprint, render_template, redirect, url_for, request, flash
from itsdangerous import URLSafeTimedSerializer as URLSerializer
from itsdangerous import SignatureExpired, BadTimeSignature
from flask_login import *
from Attendive import db, bcrypt
from Attendive.models import *

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('main/index.html')

@main.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember_me')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User Not Found.", "danger")
            return redirect(url_for('main.register'))
        if bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True if remember=='on' else False, duration=timedelta(days=3))
            next_page = request.args.get('next')
            flash("User logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for('users.dashboard'))
        else:
            flash("Please check you password. Password don't match!", "danger")
            return redirect(url_for('main.login'))
    return render_template('main/login.html')

@main.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.dashboard'))
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        disclaimer = request.form.get('disclaimer')
        if not User.query.filter_by(email=email).first() and not User.query.filter_by(mobile_number=mobile_number).first():
            if password == cpassword:
                s = URLSerializer(current_app.config['SECRET_KEY'])
                token = s.dumps({"email": email, "fname": fname, "lname": lname, "mobile_number": mobile_number, "password": password, "disclaimer": disclaimer}, salt="send-email-confirmation")
                send_confirm_email(email=email, token=token)
                flash(f"An confirmation email has been sent to you on {email}!", "success")
                return redirect(url_for('main.login'))
            else:
                flash(f"Password does not match with confirm pasword!", "danger")
                return redirect(url_for('main.register'))
        else:
            flash(f"An account with {email} or {mobile_number} is already exist!", "danger")
            return redirect(url_for('main.login'))
    return render_template('main/register.html')

@main.route('/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    return render_template('main/forgot_password.html')

@main.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():
    return render_template('main/reset_password.html')
