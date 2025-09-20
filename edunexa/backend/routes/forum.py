# routes/forum.py
from flask import Blueprint, render_template, request, jsonify, session
from utils.auth_decorators import login_required

forum_bp = Blueprint('forum', __name__)

@forum_bp.route('/')
@login_required
def forum_home():
    # Example response
    return render_template('forum/list.html')

@forum_bp.route('/<topic_id>')
@login_required
def forum_topic(topic_id):
    # Example response
    return f"Forum topic {topic_id} details"
