from flask import Flask, render_template, session, redirect, request, url_for, flash, jsonify
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import os
from dotenv import load_dotenv
from datetime import datetime
import calendar
import json

load_dotenv()  # .env file load करो

# Sirf yahan se import karo
from modules.models import db

# ⚠️ Global variables - SIRF EK BAAR DEFINE KARO
bcrypt = Bcrypt()
limiter = None  # Global variable

def create_app():
    global limiter
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'zone-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zone.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CSRF Protection
    csrf = CSRFProtect(app)
    
    # Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["2000 per day", "500 per hour", "10 per second"]
    )
    
    # Security Headers
    talisman = Talisman(
        app,
        force_https=False, 
        content_security_policy=None
    )
    
    @app.after_request
    def add_security_headers(response):
        # Market pages ke liye strict security nahi lagao
        if request.path.startswith('/market-live'):
            return response
        # Baaki sab pages ke liye security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
     
    # Session Security
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=3600
    )
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # ⚠️ LOGIN MANAGER - YAHAN INITIALIZE KARO
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # ⚠️ USER LOADER - YEH FUNCTION FLASK-LOGIN KE LIYE ZAROORI HAI
    @login_manager.user_loader
    def load_user(user_id):
        from modules.models import User
        return User.query.get(int(user_id))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Import blueprints (yahan import karo)
    from modules.auth import auth_bp
    from modules.payment import payment_bp
    from modules.travel import travel_bp
    from modules.fastag import fastag_bp
    from modules.rewards import rewards_bp 
    from modules.bills import bills_bp
    from modules.entertainment import entertainment_bp
    from modules.shopping import shopping_bp
    from modules.insurance import insurance_bp
    from modules.cibil import cibil_bp
    from modules.ott import ott_bp
    from modules.language import language_bp
    from modules.market import market_bp
    from modules.gov import gov_bp 
    from modules.ai_assistant import ai_bp 
    from modules.bharat import bharat_bp 
    from modules.heritage import heritage_bp
    from modules.market_live import market_live_bp
    from modules.simple_market import simple_market_bp
    from news_notifier import news_bp, start_news_thread
    from modules.auth import auth_bp, init_oauth

     # Initialize OAuth for social login
    init_oauth(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(fastag_bp)
    app.register_blueprint(rewards_bp)
    app.register_blueprint(travel_bp)
    app.register_blueprint(bills_bp)
    app.register_blueprint(entertainment_bp)
    app.register_blueprint(shopping_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(cibil_bp)
    app.register_blueprint(ott_bp)
    app.register_blueprint(language_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(gov_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(bharat_bp) 
    app.register_blueprint(heritage_bp, url_prefix='/bharat')
    app.register_blueprint(market_live_bp)
    app.register_blueprint(simple_market_bp)
    app.register_blueprint(news_bp) 
     
 
    # 🆕 START NEWS THREAD - YEH LINE ADD KARO
    start_news_thread()
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html', title='Zone Home')
    
    @app.route('/set-theme/<theme>')
    def set_theme(theme):
        if theme in ['orange', 'light', 'dark']:
            session['theme'] = theme
        return redirect(request.referrer or url_for('index'))
    
    @app.route('/about')
    def about():
        return render_template('about.html', title='About Zone')
    
    @app.route('/services')
    def services():
        return render_template('services.html', title='Our Services')
   
    @app.route('/api/select-plan', methods=['POST'])
    def select_plan():
        data = request.get_json()
        print(f"Plan selected: {data}")
        return jsonify({'success': True})
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name')
            flash(f'Thank you {name}! Your message has been sent!', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', title='Contact Zone')
    
    # ========== API endpoint for AI chat with real-time info ==========
    @app.route('/api/chat', methods=['POST'])
    def chat():
        try:
            data = request.get_json()
            user_message = data.get('message', '').lower()
            
            # Check if user is asking about current day/date/time
            time_keywords = ['दिन', 'डेट', 'date', 'तारीख', 'कौन सा दिन', 'आज कौन सा दिन', 
                            'today', 'what day', 'current date', 'आज की तारीख', 'समय', 'time']
            
            if any(keyword in user_message for keyword in time_keywords):
                # Return real-time date without calling AI
                now = datetime.now()
                day_name = calendar.day_name[now.weekday()]
                # Hindi day names
                hindi_days = {
                    'Monday': 'सोमवार', 'Tuesday': 'मंगलवार', 'Wednesday': 'बुधवार',
                    'Thursday': 'गुरुवार', 'Friday': 'शुक्रवार', 'Saturday': 'शनिवार',
                    'Sunday': 'रविवार'
                }
                hindi_day = hindi_days.get(day_name, day_name)
                date_str = now.strftime("%d %B %Y")
                
                reply = f"आज {hindi_day} है, {date_str}।"
                return jsonify({'reply': reply})
            
            # For other queries, call Groq API
            import requests
            
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                return jsonify({'reply': "API key नहीं मिली। कृपया .env फाइल में GROQ_API_KEY सेट करें।"})
            
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {
                        "role": "system",
                        "content": "तुम एक सहायक AI हो। तुम्हारा नाम 'ज़ी' है। तुम हिंदी और अंग्रेजी दोनों में जवाब दे सकती हो। अगर कोई सवाल तुम्हारी जानकारी से बाहर हो (December 2023 के बाद का), तो ईमानदारी से बता देना कि तुम्हें नहीं पता।"
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                return jsonify({'reply': reply})
            else:
                return jsonify({'reply': f"Error: {response.status_code} - {response.text}"})
                
        except Exception as e:
            return jsonify({'reply': f"क्षमा करें, कुछ गड़बड़ हो गई: {str(e)}"})
    
    # ========== BHARAT REDIRECT ==========
    @app.route('/bharat')
    @app.route('/bharat/')
    def bharat_redirect():
        return redirect('/heritage/')
    
    return app

app = create_app()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)