from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from Attendive.models import *

admin = Blueprint('admin', __name__)

@admin.route('/admin/approve_leaves/')
@login_required
def approve_leaves():
    applications = Application.query.filter_by(status='REQUESTED').all()
    id_ = request.args.get('id')
    status = request.args.get('status')
    if id_:
        application = Application.query.filter_by(id=id_).first()
        application.status = status
        db.session.commit()
        flash(f"Application updated with {status}", "success")
        return redirect(url_for('admin.approve_leaves'))
    return render_template('admin/approve_leaves.html', applications=applications)

@admin.route('/admin/approved_leaves/')
@login_required
def approved_leaves():
    applications = Application.query.filter_by(status='APPROVED').all()
    return render_template('admin/approved_leaves.html', applications=applications)

@admin.route('/admin/rejected_leaves/')
@login_required
def rejected_leaves():
    applications = Application.query.filter_by(status='REJECTED').all()
    return render_template('admin/rejected_leaves.html', applications=applications)

@admin.route('/admin/allocate_faculty/', methods=['GET', 'POST'])
@login_required
def allocate_faculty():
    subjects = Subject.query.all()
    role = Role.query.filter_by(name='faculty').first()
    faculties = role.user
    if request.method == "POST":
        # Getting data from frontend
        faculty_id = request.form.get('faculty_id')
        section = request.form.get('section')
        subject = request.form.get('subject')
        # Selected Subject
        allocate_subject = Subject.query.filter_by(name=subject).first()
        # all studets having sesion=section
        students = User.query.filter_by(section=section).filter_by(semester=allocate_subject.semester).all()
        # Faculty
        faculty_user = User.query.filter_by(id=faculty_id).first()
        # Add subject to faculty
        faculty_user.subjects.append(allocate_subject)
        db.session.commit()
        for student in students:
            student.subjects.append(allocate_subject)
            db.session.commit()
        flash(f"Faculty allocated with selected subject {subject}", "success")
        return redirect(url_for('admin.allocate_faculty'))
    return render_template('admin/allocate_faculty.html', subjects=subjects, faculties=faculties)

@admin.route('/admin/faculty_list/', methods=['GET', 'POST'])
@login_required
def faculty_list():
    role = Role.query.filter_by(name='faculty').first()
    faculties = role.user
    return render_template('admin/faculty_list.html', faculties=faculties)

@admin.route('/admin/students_list/', methods=['GET', 'POST'])
@login_required
def students_list():
    role = Role.query.filter_by(name='student').first()
    students = role.user
    id_ = request.args.get('id')
    status = request.args.get('status')
    if id_:
        status_pev = status
        if status == 'APPROVED':
            status = True
        elif status == 'REJECTED':
            status = None
        student = User.query.filter_by(id=id_).first()
        student.is_approved = status
        db.session.commit()
        flash(f"Student {status_pev}.","success")
        return redirect(url_for('admin.students_list'))
    return render_template('admin/students_list.html', students=students)
