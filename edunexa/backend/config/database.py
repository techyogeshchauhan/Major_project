from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'edunexa')

client = None
db = None

def init_db():
    global client, db
    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        
        # Test connection
        client.admin.command('ping')
        print("MongoDB connected successfully!")
        
        # Create indexes
        create_indexes()
        
    except Exception as e:
        print(f"Database connection error: {e}")

def get_db():
    return db

def create_indexes():
    """Create database indexes for better performance"""
    try:
        # User indexes
        db.users.create_index([("email", 1)], unique=True)
        db.users.create_index([("role", 1)])
        
        # Course indexes
        db.courses.create_index([("instructor_id", 1)])
        db.courses.create_index([("created_at", -1)])
        
        # Chat history indexes
        db.chat_history.create_index([("user_id", 1), ("created_at", -1)])
        
        print("Database indexes created successfully!")
    except Exception as e:
        print(f"Error creating indexes: {e}")