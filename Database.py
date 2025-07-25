from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class VerificationCode(db.Model):
    __tablename__ = 'verification_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<VerificationCode {self.email}>'
    
class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.String(32), primary_key=True, nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    total_prompt_tokens = db.Column(db.Integer, nullable=True)
    total_completion_tokens = db.Column(db.Integer, nullable=True)
    total_tokens = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    title = db.Column(db.String(128), nullable=True)
    title_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.String(32), primary_key=True, nullable=False)
    chat_id = db.Column(db.String(32), db.ForeignKey('chats.id'), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(16), nullable=False)
    finish_reason = db.Column(db.String(32), nullable=True)
    prompt_tokens = db.Column(db.Integer, nullable=False, default=0)
    completion_tokens = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    message_type = db.Column(db.String(16), nullable=False, default='common')

class Itinerary(db.Model):
    __tablename__ = 'itineraries'
    id = db.Column(db.String(32), primary_key=True)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class ItineraryDetail(db.Model):
    __tablename__ = 'itinerary_details'
    id = db.Column(db.String(32), primary_key=True)
    itinerary_id = db.Column(db.String(32), db.ForeignKey('itineraries.id'), nullable=False)
    location_name = db.Column(db.String(128), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

if __name__ == '__main__':
    password