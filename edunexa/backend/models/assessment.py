# routes/assessments.py
from flask import Blueprint, render_template, request, jsonify, session
from utils.auth_decorators import login_required

assessments_bp = Blueprint('assessments', __name__)

@assessments_bp.route('/')
@login_required
def list_assessments():
    # Example response
    return render_template('assessments/list.html')

@assessments_bp.route('/<assessment_id>')
@login_required
def assessment_detail(assessment_id):
    # Example response
    return f"Details for assessment {assessment_id}"

@assessments_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_assessment():    
    # Example response
    return render_template('assessments/create.html')