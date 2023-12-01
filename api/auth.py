""" Objects that handle all default RestFul API actions for Users:
    - Signup
    - Login
    - Logout
    - User chat Session
"""
from validate_email import validate_email
from flask import flash, render_template, url_for, redirect, session, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from models.users import User
from database import db

# BLUEPRINT
auth = Blueprint('auth', __name__, url_prefix='/auth')


def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session


@auth.before_request
def require_login():
    protected_routes = ['/chat']
    if request.path in protected_routes and not is_authenticated():
        flash('Kindly login to access generate')
        return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'], strict_slashes=False)
def signup():
    """Signup logic"""
    if request.method == 'POST':
        email = request.form.get('email')

        if not validate_email(email, check_mx=False):
            invalid_credential = 'Invalid Credentials'
            flash(invalid_credential)

        password_hash = generate_password_hash(request.form.get('password'))
        username = request.form.get('username')

        existing_user = db.session.query(User).filter_by(email=email).first()
        try:
            if existing_user:
                signup_message = 'An account with this email already exists. Try logging in?'
                return signup_message
            elif not email or not password_hash:
                credential_error = 'Missing credentials.'
                flash(credential_error)
                
            else:
                new_user = User(email=email,
                                password_hash=password_hash,
                                username=username)

                db.session.add(new_user)
                db.session.commit()
                login_success = 'Account created successfully. Redirecting to login.'
                flash(login_success)
                return render_template('login.html')
        except Exception as e:
            print(f"Exception: {e}")
            db.session.rollback()
            internal_error = 'There was a problem creating your account. Try again.'
            flash(internal_error)
            return redirect('/signup')


@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Login Logic"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            message = 'Oops, Looks like you do not have an account. Kindly create one.'
            flash(message)
        elif not check_password_hash(user.password_hash, password):
            incorrect_password = 'Incorrect password. Please try again!'
            flash(incorrect_password)
            return redirect(url_for('auth.login'))
        else:
            session['user_id'] = user.id
            login_success = f'Welcome {user.username}'
            flash(login_success)
            return redirect(url_for('home'))
    return render_template('login.html')


@auth.route('/logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """Logout logic"""
    session.pop('user_id', None)
    message = 'You have been logged out successfully.'
    flash(message)
    return redirect(url_for('auth.login'))
