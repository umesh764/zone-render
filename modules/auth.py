from authlib.integrations.flask_client import OAuth
import os
from twilio.rest import Client
from flask_mail import Mail, Message
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from extensions import limiter
from modules.models import db, User, OTPVerification
import random
import re
from datetime import datetime, timedelta

# Blueprint banayein
auth_bp = Blueprint('auth', __name__)

# Initialize extensions
bcrypt = Bcrypt()
login_manager = LoginManager()

# ⚠️ SIRF EK USER_LOADER HONA CHAHIYE
@login_manager.user_loader
def load_user(user_id):
    from modules.models import User
    return User.query.get(int(user_id))
    

# Helper function to send OTP
def send_otp_sms(phone, otp):
    print(f"Sending OTP {otp} to {phone}")
    return True

def generate_otp():
    return str(random.randint(100000, 999999))

def validate_phone(phone):
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, phone)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not validate_phone(phone):
            flash('Please enter a valid 10-digit mobile number', 'error')
            return render_template('register.html')
        
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            flash('This phone number is already registered', 'error')
            return render_template('register.html')
        
        otp = generate_otp()
        
        otp_entry = OTPVerification(
            phone=phone,
            otp=otp,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(otp_entry)
        db.session.commit()
        
        send_otp_sms(phone, otp)
        
        session['reg_phone'] = phone
        session['reg_name'] = name
        session['reg_email'] = email
        session['reg_password'] = bcrypt.generate_password_hash(password).decode('utf-8')
        
        flash(f'OTP sent to {phone}', 'success')
        return redirect(url_for('auth.verify_otp'))
    
    return render_template('register.html')

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@auth_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        otp = request.form.get('otp')
        phone = session.get('reg_phone')
        
        otp_entry = OTPVerification.query.filter_by(
            phone=phone, 
            otp=otp,
            is_used=False
        ).first()
        
        if otp_entry and otp_entry.expires_at > datetime.utcnow():
            otp_entry.is_used = True
            
            user = User(
                phone=phone,
                name=session.get('reg_name'),
                email=session.get('reg_email'),
                password=session.get('reg_password'),
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()
            
            session.pop('reg_phone', None)
            session.pop('reg_name', None)
            session.pop('reg_email', None)
            session.pop('reg_password', None)
            
            login_user(user)
            
            flash('Registration successful! Welcome to Zone.', 'success')
            return redirect(url_for('payment.dashboard'))
        else:
            flash('Invalid or expired OTP', 'error')
    
    return render_template('verify-otp.html')

# Twilio client initialization
twilio_client = Client(
    os.environ.get('TWILIO_ACCOUNT_SID'),
    os.environ.get('TWILIO_AUTH_TOKEN')
)
VERIFY_SERVICE_SID = os.environ.get('TWILIO_VERIFY_SERVICE')

def send_whatsapp_otp(phone_number):
    """WhatsApp par OTP bhejne ke liye"""
    try:
        verification = twilio_client.verify.services(VERIFY_SERVICE_SID).verifications.create(
            to=phone_number,
            channel='whatsapp'
        )
        return verification.status == 'pending'
    except Exception as e:
        print(f"WhatsApp OTP error: {e}")
        return False

def send_email_otp(email_address):
    """Email par OTP bhejne ke liye"""
    try:
        verification = twilio_client.verify.services(VERIFY_SERVICE_SID).verifications.create(
            to=email_address,
            channel='email'
        )
        return verification.status == 'pending'
    except Exception as e:
        print(f"Email OTP error: {e}")
        return False

def verify_otp(contact, code):
    """OTP verify karne ke liye"""
    try:
        verification_check = twilio_client.verify.services(VERIFY_SERVICE_SID).verification_checks.create(
            to=contact,
            code=code
        )
        return verification_check.status == 'approved'
    except Exception as e:
        print(f"OTP verify error: {e}")
        return False

# OAuth setup
oauth = None  # Global variable

def init_oauth(app):
    global oauth
    oauth = OAuth(app)
    
    # Google OAuth
   oauth.register(
        name='google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )
    
    # Facebook OAuth
    oauth.register(
        name='facebook',
        client_id=os.environ.get('FACEBOOK_CLIENT_ID'),
        client_secret=os.environ.get('FACEBOOK_CLIENT_SECRET'),
        authorize_url='https://www.facebook.com/v18.0/dialog/oauth',
        access_token_url='https://graph.facebook.com/v18.0/oauth/access_token',
        api_base_url='https://graph.facebook.com/v18.0/',
        client_kwargs={'scope': 'email public_profile'}
    )
    
    # GitHub OAuth
    oauth.register(
        name='github',
        client_id=os.environ.get('GITHUB_CLIENT_ID'),
        client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
        authorize_url='https://github.com/login/oauth/authorize',
        access_token_url='https://github.com/login/oauth/access_token',
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'}
    )

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        user = User.query.filter_by(phone=phone).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('payment.dashboard'))
        else:
            flash('Invalid phone number or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        # Add your forgot password logic here
        flash('Password reset link sent to your email', 'success')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')

@auth_bp.route('/resend-otp')
def resend_otp():
    phone = session.get('reg_phone')
    if phone:
        otp = generate_otp()
        
        otp_entry = OTPVerification(
            phone=phone,
            otp=otp,
            expires_at=datetime.utcnow() + timedelta(minutes=10)
        )
        db.session.add(otp_entry)
        db.session.commit()
        
        send_otp_sms(phone, otp)
        
        flash('New OTP sent successfully', 'success')
    return redirect(url_for('auth.verify_otp'))

# Google Login Routes
@auth_bp.route('/login/google')
def google_login():
    global oauth
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/authorized')
def google_authorize():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    
    email = user_info.get('email')
    name = user_info.get('name')
    
    return handle_social_login(email, name, 'google')

# Facebook Login Routes
@auth_bp.route('/login/facebook')
def facebook_login():
    global oauth
    redirect_uri = url_for('auth.facebook_authorize', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@auth_bp.route('/login/facebook/authorized')
def facebook_authorize():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get('me?fields=id,name,email')
    user_info = resp.json()
    
    email = user_info.get('email')
    name = user_info.get('name')
    
    return handle_social_login(email, name, 'facebook')

# GitHub Login Routes
@auth_bp.route('/login/github')
def github_login():
    global oauth
    redirect_uri = url_for('auth.github_authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@auth_bp.route('/login/github/authorized')
def github_authorize():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user')
    user_info = resp.json()
    
    email = user_info.get('email')
    name = user_info.get('name', user_info.get('login'))
    
    return handle_social_login(email, name, 'github')

# Common function to handle all social logins
def handle_social_login(email, name, provider):
    if not email:
        flash(f'Could not get email from {provider}. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Check if user exists
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Create new user
        user = User(
            name=name or email.split('@')[0],
            email=email,
            password=None,  # Social login users don't need password
            is_verified=True,
            provider=provider
        )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created with {provider}!', 'success')
    
    login_user(user)
    flash(f'Logged in with {provider}!', 'success')
    return redirect(url_for('payment.dashboard'))