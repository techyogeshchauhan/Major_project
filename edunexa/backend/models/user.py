from werkzeug.security import generate_password_hash, check_password_hash
from config.database import get_db
from bson.objectid import ObjectId
from datetime import datetime

class User:
    def __init__(self, name=None, email=None, password=None, role='student'):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password) if password else None
        self.role = role  # 'student', 'instructor', 'admin'
        self.created_at = datetime.utcnow()
        self.is_active = True
        self.profile_image = None
        self.bio = ""
    
    def save(self):
        """Save user to database"""
        db = get_db()
        user_data = {
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at,
            'is_active': self.is_active,
            'profile_image': self.profile_image,
            'bio': self.bio
        }
        
        result = db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    def check_password(self, password):
        """Check if provided password matches user's password"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = get_db()
        user_data = db.users.find_one({'email': email})
        
        if user_data:
            user = User()
            user.id = str(user_data['_id'])
            user.name = user_data['name']
            user.email = user_data['email']
            user.password_hash = user_data['password_hash']
            user.role = user_data['role']
            user.created_at = user_data['created_at']
            user.is_active = user_data.get('is_active', True)
            user.profile_image = user_data.get('profile_image')
            user.bio = user_data.get('bio', "")
            return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        db = get_db()
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        
        if user_data:
            user = User()
            user.id = str(user_data['_id'])
            user.name = user_data['name']
            user.email = user_data['email']
            user.role = user_data['role']
            user.is_active = user_data.get('is_active', True)
            user.profile_image = user_data.get('profile_image')
            user.bio = user_data.get('bio', "")
            return user
        return None