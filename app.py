"""Application entry point"""
import os
from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from database import db
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = ''

db.init_app(app)

migrate = Migrate(app, db)

from models import user
from api.yi import chat
from api.auth import auth

app.register_blueprint(chat)
app.register_blueprint(auth)

