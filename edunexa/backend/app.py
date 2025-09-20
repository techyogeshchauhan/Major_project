from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from config.database import init_db
from routes.auth import auth_bp
from routes.chatbot import chatbot_bp
from routes.courses import courses_bp
from routes.assessments import assessments_bp
from routes.forum import forum_bp
from routes.progress import progress_bp
from utils.helpers import allowed_file
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'videos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'pdfs'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
    
    # Initialize CORS
    CORS(app, supports_credentials=True)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(assessments_bp, url_prefix='/api/assessments')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    
    # Main routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user_role = session.get('role', 'student')
        template = f'dashboard/{user_role}.html'
        return render_template(template)
    
    @app.route('/chatbot')
    def chatbot_interface():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('chatbot/interface.html')
    
    @app.route('/courses')
    def courses_list():
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('courses/list.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)