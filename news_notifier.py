import time
import threading
from datetime import datetime
from flask import Blueprint, jsonify

news_bp = Blueprint('news', __name__)

latest_news = [
    {"title": "📰 भारत ने नया रिकॉर्ड बनाया", "source": "News18", "url": "https://www.news18.com"},
    {"title": "💰 महाराष्ट्र में नई योजना लॉन्च", "source": "Zee News", "url": "https://zeenews.india.com"},
    {"title": "🚗 Nagpur में स्मार्ट सिटी प्रोजेक्ट", "source": "Lokmat", "url": "https://www.lokmat.com"},
    {"title": "🌤️ आज का मौसम: गर्मी से राहत नहीं", "source": "ABP News", "url": "https://www.abplive.com"},
    {"title": "📱 डिजिटल इंडिया की नई पहल", "source": "Times Now", "url": "https://www.timesnownews.com"},
    {"title": "🏏 IPL 2026: आज के मैच का शेड्यूल", "source": "Sports Tak", "url": "https://www.sportstak.com"},
    {"title": "🏦 बैंकों की नई EMI योजना", "source": "Business Standard", "url": "https://www.business-standard.com"},
    {"title": "🚂 रेलवे ने शुरू की नई ट्रेन", "source": "Rail News", "url": "https://www.indianrail.gov.in"},
    {"title": "📚 स्कूलों में नई शिक्षा नीति", "source": "Education Times", "url": "https://www.educationtimes.com"},
    {"title": "🏥 स्वास्थ्य योजना का विस्तार", "source": "Health News", "url": "https://www.health.com"}
]

@news_bp.route('/api/news/latest')
def get_latest_news():
    return jsonify({
        "status": "ok",
        "news": latest_news
    })

def start_news_thread():
    def background_task():
        print("News background task started")
        while True:
            print("News available: " + str(len(latest_news)) + " items")
            time.sleep(60)
    
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()
    print("News notification thread started")