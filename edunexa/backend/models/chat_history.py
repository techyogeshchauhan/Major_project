# models/chat_history.py
from pymongo import MongoClient
import datetime
import os

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['edunexa_db']  # database name

class ChatHistory:
    collection = db['chat_history']

    @staticmethod
    def save_message(user_id, message, response):
        doc = {
            'user_id': user_id,
            'message': message,
            'response': response,
            'timestamp': datetime.datetime.utcnow()
        }
        return ChatHistory.collection.insert_one(doc)

    @staticmethod
    def get_history(user_id, limit=50):
        return list(ChatHistory.collection.find({'user_id': user_id}).sort('timestamp', -1).limit(limit))
