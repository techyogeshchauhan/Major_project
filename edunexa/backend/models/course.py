from datetime import datetime
from bson import ObjectId
from config.database import MongoDBManager, COURSES_COLLECTION

class Course:
    @staticmethod
    def create_course(title, description, instructor_id, category, **kwargs):
        db = MongoDBManager.get_db()
        
        course_data = {
            'title': title,
            'description': description,
            'instructor_id': ObjectId(instructor_id),
            'category': category,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_published': False,
            'modules': [],
            'enrolled_students': [],
            **kwargs
        }
        
        result = db[COURSES_COLLECTION].insert_one(course_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_id(course_id):
        db = MongoDBManager.get_db()
        return db[COURSES_COLLECTION].find_one({'_id': ObjectId(course_id)})
    
    @staticmethod
    def find_all(published_only=True):
        db = MongoDBManager.get_db()
        query = {'is_published': True} if published_only else {}
        return list(db[COURSES_COLLECTION].find(query))
    
    @staticmethod
    def find_by_instructor(instructor_id):
        db = MongoDBManager.get_db()
        return list(db[COURSES_COLLECTION].find({'instructor_id': ObjectId(instructor_id)}))
    
    @staticmethod
    def update_course(course_id, update_data):
        db = MongoDBManager.get_db()
        update_data['updated_at'] = datetime.utcnow()
        result = db[COURSES_COLLECTION].update_one(
            {'_id': ObjectId(course_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def enroll_student(course_id, student_id):
        db = MongoDBManager.get_db()
        result = db[COURSES_COLLECTION].update_one(
            {'_id': ObjectId(course_id)},
            {'$addToSet': {'enrolled_students': ObjectId(student_id)}}
        )
        return result.modified_count > 0