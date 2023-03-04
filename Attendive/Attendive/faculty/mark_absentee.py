import sys
sys.path.insert(0, 'D:\\STUDY\\B. TECH\\4th Year\\7th Sem\\Face Detection Attendance System\\Attendive')

from Attendive import db, create_app
from Attendive.models import *
from datetime import datetime, timedelta, date
import pytz

app = create_app()
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
tz = pytz.timezone('Asia/Calcutta')

attendances = Attendance.query.filter_by(status='NA').all()

for attendance in attendances:
    marked_attendance_date = attendance.marked_attendance.replace(tzinfo=pytz.utc)
    if marked_attendance_date+timedelta(minutes=3) <= datetime.now(tz).replace(tzinfo=pytz.utc):
        user_id = attendance.user_id
        user = User.query.filter_by(id=user_id).first()
        applications_list = [appl for appl in list(user.applications) if appl.application_type == 'LEAVE']
        for application in applications_list:
            if (application.status == 'APPROVED') and application.total_days_left > 0:
                if datetime.now(tz).date() >= application.leave_from and datetime.now(tz).date() <= application.leave_till:
                    attendance.status = 'L'
                    application.total_days_left -= 1
                    db.session.commit()
            if (application.status == 'REJECTED') and application.total_days_left > 0:
                if datetime.now(tz).date() >= application.leave_from and datetime.now(tz).date() <= application.leave_till:
                    attendance.status = 'A'
                    application.total_days_left = 0
                    db.session.commit()
        applications_list = [appl for appl in list(user.applications) if appl.application_type == 'WORK ATTENDANCE']
        for application in applications_list:
            if (application.status == 'APPROVED') and application.total_days_left > 0:
                if datetime.now(tz).date() >= application.leave_from and datetime.now(tz).date() <= application.leave_till:
                    attendance.status = 'P'
                    application.total_days_left -= 1
                    db.session.commit()
            if (application.status == 'REJECTED') and application.total_days_left > 0:
                if datetime.now(tz).date() >= application.leave_from and datetime.now(tz).date() <= application.leave_till:
                    attendance.status = 'A'
                    application.total_days_left = 0
                    db.session.commit()
                    pass
        if attendance.status == 'NA':
            attendance.status = 'A'
            db.session.commit()
