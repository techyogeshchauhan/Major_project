from flask import Blueprint, request, jsonify, session
from models.user import User
from utils.auth_decorators import login_required
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'student')
        
        if not all([name, email, password]):
            return jsonify({'error': 'Name, email and password are required'}), 400
        
        user_id, error = User.create_user(name, email, password, role)
        if error:
            return jsonify({'error': error}), 409
        
        return jsonify({
            'message': 'User created successfully',
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.find_by_email(email)
        if not user or not User.verify_password(user['password'], password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.get('is_active', True):
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Set session
        session['user_id'] = str(user['_id'])
        session['user_role'] = user['role']
        session['user_name'] = user['name']
        session.permanent = True
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    try:
        user_id = session.get('user_id')
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user['role'],
                'created_at': user['created_at'].isoformat() if user.get('created_at') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500