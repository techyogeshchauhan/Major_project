import os
from datetime import timedelta

class Config:
    # Basic Flask Config
    SECRET_KEY = os.getenv('SECRET_KEY', 'edunexa-secret-key-2025')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # File Upload
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/edunexa_dev')

class ProductionConfig(Config):
    DEBUG = False
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/edunexa')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}