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

from models import users
from api.yi import chat
from api.auth import auth

app.register_blueprint(chat)
app.register_blueprint(auth)

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/sign_up')
def signup_page():
    """Sign Up Page"""
    return render_template('signup.html')

@app.route('/log_in')
def login_page():
    """Log in Page"""
    return render_template('login.html')

@app.route('/chat')
def home():
    """Home Page - generate"""
    return render_template('generate.html')


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
