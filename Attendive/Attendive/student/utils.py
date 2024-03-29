from Attendive import mail
from flask_mail import Message
from flask import url_for, current_app
from PIL import Image
import secrets
import os


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=('Attendive', 'support@tejearning.com'), recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link. The link will expire in 10 minutes:
{url_for('student.reset_token', token=token, _external=True)}

If your did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_confirm_email(email, token):
    msg = Message('Confirm Your Account',
                  sender=('Attendive', 'support@tejearning.com'), recipients=[email])
    msg.body = f'''To confirm your email, visit the following link. The link will expire in 10 minutes:
{url_for('student.confirm_email', token=token, _external=True)}

'''
    mail.send(msg)

def save_picture(id_, form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    if f_ext not in ['.png', '.jpg', '.jpeg']:
        return None
    picture_fn = str(id_) + f_ext
    picture_path = os.path.join(current_app.root_path, f'student\pic\\', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn
