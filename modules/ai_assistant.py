from flask import Blueprint, render_template, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
import feedparser
import json
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime, timedelta

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')

# ============================================
# होम पेज - AI Assistant
# ============================================
@ai_bp.route('/')
def ai_home():
    """AI Assistant Home Page"""
    return render_template('ai/assistant.html')

# ============================================
# टेक्स्ट क्वेरी API (अपडेटेड)
# ============================================
@ai_bp.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    # Debug: Check if API key is loaded
    api_key = os.environ.get('GROQ_API_KEY')
    print(f"🔑 DEBUG - GROQ_API_KEY exists: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"🔑 DEBUG - API Key starts with: {api_key[:10]}...")
    
    # ⬇️⬇️⬇️ नया भाग यहाँ से शुरू ⬇️⬇️⬇️
    
    # ताजा खबरों के लिए check करें
    if any(word in question.lower() for word in ['ताजा खबर', 'न्यूज', 'news', 'latest', 'आज की खबर', 'update']):
        news = get_latest_news()
        if news:
            answer = format_news_response(news)
            return jsonify({
                'question': question,
                'answer': answer,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    # 2026 या नई जानकारी के लिए वेब सर्च
    if any(word in question.lower() for word in ['2026', 'नया', 'latest', 'trending', 'upcoming', 'क्या चल रहा']):
        web_results = search_web_live(question)
        if web_results:
            context = format_web_results(web_results)
            enhanced_question = f"{context}\n\nइस जानकारी के आधार पर सवाल का जवाब दो: {question}"
            answer = get_ai_response(enhanced_question)
            return jsonify({
                'question': question,
                'answer': answer,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    # ⬆️⬆️⬆️ नया भाग यहाँ समाप्त ⬆️⬆️⬆️
    
    # अगर कुछ खास नहीं, तो सीधे AI से पूछें
    answer = get_ai_response(question)
    
    return jsonify({
        'question': question,
        'answer': answer,
        'timestamp': datetime.utcnow().isoformat()
    })


    # ======================================================
    # ⚠️ यहाँ से नई चीजें जोड़ें ⚠️
    # ======================================================
    
    # 1. ताजा खबरों के लिए check करें
    if any(word in question.lower() for word in ['ताजा खबर', 'न्यूज', 'news', 'latest', 'आज की खबर', 'update']):
        news = get_latest_news()
        if news:
            answer = format_news_response(news)
            return jsonify({
                'question': question,
                'answer': answer,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    # 2. 2026 या नई जानकारी के लिए वेब सर्च
    if any(word in question.lower() for word in ['2026', 'नया', 'latest', 'trending', 'upcoming', 'क्या चल रहा']):
        web_results = search_web_live(question)
        if web_results:
            # वेब रिजल्ट्स को Groq को भेजें
            context = format_web_results(web_results)
            enhanced_question = f"{context}\n\nइस जानकारी के आधार पर सवाल का जवाब दो: {question}"
            answer = get_ai_response(enhanced_question)
            return jsonify({
                'question': question,
                'answer': answer,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    # 3. अगर कुछ खास नहीं, तो सीधे AI से पूछें
    answer = get_ai_response(question)
    
    return jsonify({
        'question': question,
        'answer': answer,
        'timestamp': datetime.utcnow().isoformat()
    })

# ============================================
# स्पीच टू टेक्स्ट API
# ============================================
@ai_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """ऑडियो फाइल से टेक्स्ट बनाएं"""
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    
    audio_file = request.files['audio']
    filename = secure_filename(f"{uuid.uuid4()}.webm")
    
    # Temp folder create करो
    os.makedirs('temp_audio', exist_ok=True)
    filepath = os.path.join('temp_audio', filename)
    audio_file.save(filepath)
    
    # Whisper से ट्रांसक्रिप्शन
    text = transcribe_with_whisper(filepath)
    
    # टेम्प फाइल डिलीट करें
    try:
        os.remove(filepath)
    except:
        pass
    
    return jsonify({'text': text})

# ============================================
# AI रिस्पॉन्स फंक्शन
# ============================================
def get_ai_response(question):
    """AI से जवाब लें"""
    
    # Option A: Groq API (फ्री, तेज़)
    groq_api_key = os.environ.get('GROQ_API_KEY')
    if groq_api_key:
        print(f"🚀 Calling Groq API with question: {question[:50]}...")
        return call_groq_api(question, groq_api_key)
    
    # Option B: OpenAI API
    openai_key = os.environ.get('OPENAI_API_KEY')
    if openai_key:
        return call_openai_api(question, openai_key)
    
    # Option C: Default response if no API key
    return "❌ API key नहीं मिली। कृपया GROQ_API_KEY सेट करें।"

def call_groq_api(question, api_key):
    """Groq API कॉल (LLaMA 3)"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",  # ✅ नया मॉडल
        'messages': [
            {'role': 'system', 'content': 'You are a helpful AI assistant for HAT PAY. Answer in Hindi or English as appropriate.'},
            {'role': 'user', 'content': question}
        ],
        'temperature': 0.7,
        'max_tokens': 500
    }
    
    try:
        print("📡 Sending request to Groq API...")
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 Groq API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            print(f"✅ Groq API success, answer length: {len(answer)}")
            return answer
        else:
            error_msg = f"Groq API error: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return f"क्षमा करें, API में समस्या है। (Error: {response.status_code})"
            
    except requests.exceptions.Timeout:
        print("❌ Groq API timeout")
        return "क्षमा करें, API ने समय सीमा पार कर दी।"
    except requests.exceptions.ConnectionError:
        print("❌ Groq API connection error")
        return "क्षमा करें, API से कनेक्ट नहीं हो सका।"
    except Exception as e:
        print(f"❌ Groq API unexpected error: {str(e)}")
        return f"क्षमा करें, कुछ गड़बड़ हो गई। (Error: {str(e)})"

def call_openai_api(question, api_key):
    """OpenAI API कॉल"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful AI assistant for HAT PAY.'},
            {'role': 'user', 'content': question}
        ],
        'temperature': 0.7,
        'max_tokens': 500
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            return f"OpenAI API error: {response.status_code}"
    except Exception as e:
        return f"OpenAI API error: {str(e)}"

def transcribe_with_whisper(audio_path):
    """Whisper से ऑडियो ट्रांसक्राइब करें"""
    try:
        # Try to import whisper
        try:
            import whisper
            print("🎤 Loading Whisper model...")
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            text = result['text'].strip()
            print(f"🎤 Transcription successful: {text[:50]}...")
            return text
        except ImportError:
            print("❌ Whisper not installed")
            return "Whisper library not installed. Please install with: pip install openai-whisper"
    except Exception as e:
            print(f"❌ Transcription error: {str(e)}")
            return "ऑडियो प्रोसेसिंग में समस्या हुई। कृपया टाइप करके पूछें।"
# ============================================
# न्यूज और वेब सर्च के लिए हेल्पर फंक्शन
# ============================================

# न्यूज सोर्सेज
NEWS_SOURCES = {
    'pib': 'https://pib.gov.in/RssMain.aspx',
    'mygov': 'https://www.mygov.in/rss/news/',
    'nasscom': 'https://www.nasscom.in/rss.xml'
}

# कैश
news_cache = {}
cache_expiry = {}
CACHE_DURATION = 3600  # 1 घंटा

def format_news_response(news_items):
    """न्यूज को खूबसूरत फॉर्मेट में दिखाएं"""
    response = "📰 **ताजा खबरें**\n\n"
    for i, item in enumerate(news_items[:5], 1):
        response += f"**{i}. {item['title']}**\n"
        response += f"   {item['summary']}\n"
        response += f"   📌 {item['source']} | 🕒 {item['date']}\n\n"
    return response

def format_web_results(results):
    """वेब सर्च रिजल्ट्स को फॉर्मेट करें"""
    context = "मैंने इंटरनेट से यह जानकारी ली है:\n\n"
    for result in results:
        context += f"• **{result['title']}**\n"
        context += f"  {result['snippet']}\n"
        context += f"  🔗 {result['link']}\n\n"
    return context

def get_latest_news(source='all'):
    """ताजा खबरें लाएं"""
    
    cache_key = f'news_{source}'
    if cache_key in news_cache:
        cache_time = cache_expiry.get(cache_key, 0)
        if datetime.now().timestamp() - cache_time < CACHE_DURATION:
            return news_cache[cache_key]
    
    all_news = []
    
    try:
        if source in ['all', 'pib']:
            feed = feedparser.parse(NEWS_SOURCES['pib'])
            for entry in feed.entries[:5]:
                all_news.append({
                    'title': entry.title,
                    'summary': entry.summary[:200] + '...' if entry.summary else '',
                    'link': entry.link,
                    'date': entry.published if hasattr(entry, 'published') else 'ताजा',
                    'source': 'PIB (सरकार)'
                })
        
        if source in ['all', 'mygov']:
            feed = feedparser.parse(NEWS_SOURCES['mygov'])
            for entry in feed.entries[:5]:
                all_news.append({
                    'title': entry.title,
                    'summary': entry.summary[:200] + '...' if entry.summary else '',
                    'link': entry.link,
                    'date': entry.published if hasattr(entry, 'published') else 'ताजा',
                    'source': 'MyGov'
                })
        
        if all_news:
            news_cache[cache_key] = all_news
            cache_expiry[cache_key] = datetime.now().timestamp()
            
    except Exception as e:
        print(f"❌ News fetch error: {str(e)}")
    
    return all_news

def search_web_live(query):
    """लाइव वेब सर्च (Google से)"""
    try:
        # Google API (अगर हो तो)
        api_key = os.environ.get('GOOGLE_API_KEY')
        cx = os.environ.get('GOOGLE_CX')
        
        if api_key and cx:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cx,
                'q': query,
                'num': 3
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get('items', []):
                    results.append({
                        'title': item['title'],
                        'snippet': item['snippet'],
                        'link': item['link']
                    })
                return results
    except Exception as e:
        print(f"❌ Search error: {str(e)}")
    
    return []