# routes/courses.py
from flask import Blueprint, render_template, request, jsonify, session
from utils.auth_decorators import login_required

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/')
@login_required
def list_courses():
    # Example response
    return render_template('courses/list.html')

@courses_bp.route('/<course_id>')
@login_required
def course_detail(course_id):
    # Example response
    return f"Details for course {course_id}"
