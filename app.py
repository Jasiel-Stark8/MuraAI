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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mura:aZCgqEKLKI1o51tePRmQQTGdCqapkiHh@dpg-clkd6a6rem5c73aguvcg-a/mura'
# postgresql://mura:mura@localhost:5432/mura

db.init_app(app)

migrate = Migrate(app, db)

from models import users
from api.yi import chat
from api.auth import auth
from api.save_chat import save_chat

app.register_blueprint(chat, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(save_chat)


@app.route('/')
def landing_page():
    return render_template('index.html')


@app.route('/settings')
def settings():
    return render_template('index.html')

@app.route('/signup')
def signup_page():
    """Sign Up Page"""
    return render_template('signup.html')

@app.route('/login')
def login_page():
    """Log in Page"""
    return render_template('login.html')

@app.route('/chat')
def home():
    """Home Page - generate"""
    items = [
        {'title': 'Nutrition & Diet', 'description': 'What are healthy breakfast options for someone with high cholesterol?'},
        {'title': 'Mental Health', 'description': 'What are the signs of anxiety and how can it be treated?'},
        {'title': 'Women\'s Health', 'description': 'What are the best exercises during pregnancy?'},
        {'title': 'Exercise and Fitness', 'description': 'How many steps per day are recommended for maintaining heart health?'},
        {'title': 'Cancer', 'description': 'How effective is immunotherapy in treating breast cancer?'},
        {'title': 'Diabetes', 'description': 'What are the differences between Type 1 and Type 2 diabetes?'},
    ]
    return render_template('generate.html', items=items)


if __name__ == '__main__':
    app.run()
