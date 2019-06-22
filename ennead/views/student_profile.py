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

    if g.user.student_profiles:
        student_profile = g.user.student_profiles[0]
    else:
        student_profile = StudentProfile()

    return render_template('student_profile.html', student_profile=student_profile)


@require_logged_in
def create_update_student_profile() -> Response:
    """POST /student_profile: update student profile"""

    if g.user.student_profiles:
        student_profile = g.user.student_profiles[0]
    else:
        student_profile = StudentProfile()

    for field in ('grade', 'city', 'birth_date', 'allergy', 'sex',
                  'communication', 'parent_information'):
        setattr(student_profile, field, request.form[field])

    # TODO: add telephone validation
    student_profile.telephone = request.form['telephone']

    student_profile.user = g.user

    student_profile.save()
    return redirect(url_for('read_student_profile'))

