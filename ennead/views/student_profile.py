"""Views, used for student profiles"""

from datetime import date
from ennead.models.user import User

from flask import session, current_app, render_template, request, redirect, url_for, g
from werkzeug.wrappers import Response

from ennead.utils import require_logged_in
from ennead.models.user import User, UserGroup
from ennead.models.student_profile import StudentProfile


@require_logged_in
def read_student_profile() -> Response:
    """GET /student_profile: read profile page"""

    student_profile = StudentProfile()

    student_profile_query = StudentProfile.select().where(StudentProfile.user == g.user)
    if student_profile_query.exists():
        student_profile = student_profile_query[0]

    return render_template('student_profile.html', student_profile=student_profile)


@require_logged_in
def create_update_student_profile() -> Response:
    """POST /student_profile: update student profile"""

    student_profile = StudentProfile()

    student_profile_query = StudentProfile.select().where(StudentProfile.user == g.user)
    if student_profile_query.exists():
        student_profile = student_profile_query[0]
        student_profile.set_profile(request)
    else:
        student_profile.set_profile(request, g.user)

    student_profile.save()
    return redirect(url_for('read_student_profile'))

