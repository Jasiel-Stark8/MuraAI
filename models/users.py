"""User Model for PostgreSQL database"""
from flask_sqlalchemy import SQLAlchemy
from database import db

class User(db.Model):
    """User Schema"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash
