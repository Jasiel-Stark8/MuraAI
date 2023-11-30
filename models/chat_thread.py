"""Store user chat"""
from flask_sqlalchemy import SQLAlchemy
from database import db
from models.users import User

class ChatMessage(db.Model):
    """User Chat Schema"""
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __init__(self, user_id, message_content, message_type, timestamp):
        self.user_id = user_id
        self.message_content = message_content
        self.message_type = message_type
        self.timestamp = timestamp
