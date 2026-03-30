import yfinance as yf
import sqlite3
import os
import socket
import random
from datetime import datetime
from flask import Blueprint, render_template, jsonify, request, session

market_live_bp = Blueprint('market_live', __name__, url_prefix='/market-live')

# ========== DATABASE SETUP ==========
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'zone.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT,
            quantity INTEGER,
            buy_price REAL,
            total REAL,
            buy_date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT,
            quantity INTEGER,
            sell_price REAL,
            total REAL,
            sell_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ========== OFFLINE SUPPORT ==========
def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

def get_cached_price(symbol):
    prices = {
        'RELIANCE': 2500, 'TCS': 3800, 'HDFCBANK': 1600, 'INFY': 1400,
        'ICICIBANK': 1100, 'TATAMOTORS': 980, 'SBIN': 700, 'BHARTIARTL': 1500,
        'ITC': 450, 'NTPC': 350, 'WIPRO': 550, 'HCLTECH': 1350,
        'ASIANPAINT': 3200, 'MARUTI': 12500, 'SUNPHARMA': 1700
    }
    return prices.get(symbol, 1000)

# ========== STOCK DATA ==========
STOCKS = [
    {'symbol': 'RELIANCE', 'name': 'Reliance Industries', 'sector': 'Oil & Gas'},
    {'symbol': 'TCS', 'name': 'Tata Consultancy Services', 'sector': 'IT'},
    {'symbol': 'HDFCBANK', 'name': 'HDFC Bank', 'sector': 'Banking'},
    {'symbol': 'INFY', 'name': 'Infosys', 'sector': 'IT'},
    {'symbol': 'ICICIBANK', 'name': 'ICICI Bank', 'sector': 'Banking'},
    {'symbol': 'TATAMOTORS', 'name': 'Tata Motors', 'sector': 'Auto'},
    {'symbol': 'SBIN', 'name': 'SBI', 'sector': 'Banking'},
    {'symbol': 'BHARTIARTL', 'name': 'Bharti Airtel', 'sector': 'Telecom'},
    {'symbol': 'ITC', 'name': 'ITC Limited', 'sector': 'FMCG'},
    {'symbol': 'NTPC', 'name': 'NTPC Limited', 'sector': 'Power'},
    {'symbol': 'WIPRO', 'name': 'Wipro', 'sector': 'IT'},
    {'symbol': 'HCLTECH', 'name': 'HCL Technologies', 'sector': 'IT'},
    {'symbol': 'ASIANPAINT', 'name': 'Asian Paints', 'sector': 'FMCG'},
    {'symbol': 'MARUTI', 'name': 'Maruti Suzuki', 'sector': 'Auto'},
    {'symbol': 'SUNPHARMA', 'name': 'Sun Pharma', 'sector': 'Pharma'}
]

# ========== LIVE PRICE FUNCTION ==========
def get_live_price(symbol):
    """Get live price from Yahoo Finance"""
    if check_internet():
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            hist = ticker.history(period="1d")
            if not hist.empty:
                return round(hist['Close'].iloc[-1], 2)
        except:
            pass
    return get_cached_price(symbol)

def get_all_prices():
    """Get all stock prices with change percentage"""
    prices = {}
    for stock in STOCKS:
        symbol = stock['symbol']
        current = get_live_price(symbol)
        prev = get_cached_price(symbol)
        change = round(((current - prev) / prev) * 100, 2)
        prices[symbol] = {'price': current, 'change': change}
    return prices

# ========== ROUTES ==========
@market_live_bp.route('/')
def dashboard():
    """Main Market Dashboard"""
    return render_template('market_live/dashboard.html', stocks=STOCKS, sectors=SECTORS)

@market_live_bp.route('/all-stocks')
def all_stocks():
    """All Stocks Page"""
    return render_template('market_live/all_stocks.html', stocks=STOCKS)

@market_live_bp.route('/api/nifty')
def api_nifty():
    if check_internet():
        try:
            nifty = yf.Ticker("^NSEI").history(period="1d")
            if not nifty.empty:
                return jsonify({'value': round(nifty['Close'].iloc[-1], 2)})
        except:
            pass
    return jsonify({'value': 24500})

@market_live_bp.route('/api/sensex')
def api_sensex():
    if check_internet():
        try:
            sensex = yf.Ticker("^BSESN").history(period="1d")
            if not sensex.empty:
                return jsonify({'value': round(sensex['Close'].iloc[-1], 2)})
        except:
            pass
    return jsonify({'value': 81000})

@market_live_bp.route('/api/all-prices')
def api_all_prices():
    """Get all stock prices with changes"""
    prices = get_all_prices()
    return jsonify(prices)

@market_live_bp.route('/api/stock/<symbol>')
def api_stock(symbol):
    """Get single stock price"""
    price = get_live_price(symbol)
    return jsonify({'symbol': symbol, 'price': price})

@market_live_bp.route('/api/gainers')
def api_gainers():
    """Top gainers based on percentage change"""
    prices = get_all_prices()
    gainers = []
    for symbol, data in prices.items():
        gainers.append({
            'symbol': symbol,
            'price': data['price'],
            'change': data['change']
        })
    gainers.sort(key=lambda x: x['change'], reverse=True)
    return jsonify(gainers[:5])

@market_live_bp.route('/api/losers')
def api_losers():
    """Top losers based on percentage change"""
    prices = get_all_prices()
    losers = []
    for symbol, data in prices.items():
        losers.append({
            'symbol': symbol,
            'price': data['price'],
            'change': data['change']
        })
    losers.sort(key=lambda x: x['change'])
    return jsonify(losers[:5])

@market_live_bp.route('/api/sector/<sector>')
def api_sector(sector):
    """Get stocks by sector"""
    sector_stocks = [s for s in STOCKS if s['sector'] == sector]
    result = []
    for stock in sector_stocks:
        price = get_live_price(stock['symbol'])
        result.append({
            'symbol': stock['symbol'],
            'name': stock['name'],
            'price': price
        })
    return jsonify(result)

@market_live_bp.route('/api/predict/<symbol>')
def api_predict(symbol):
    """Simple prediction based on trend"""
    price = get_live_price(symbol)
    # Simple random prediction (in real app, use ML)
    prediction = random.choice(['UP', 'DOWN', 'STABLE'])
    confidence = random.randint(60, 95)
    target = price * (1 + random.uniform(-0.05, 0.05))
    
    return jsonify({
        'symbol': symbol,
        'current_price': price,
        'prediction': prediction,
        'confidence': confidence,
        'target_price': round(target, 2)
    })

# ========== BUY/SELL ROUTES ==========
@market_live_bp.route('/buy', methods=['POST'])
def buy_stock():
    print("\n" + "="*50)
    print("🔵 BUY ROUTE HIT")
    
    try:
        data = request.get_json()
        print(f"Data: {data}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No data'}), 400
        
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        price = data.get('price')
        
        print(f"Symbol: {symbol}, Qty: {quantity}, Price: {price}")
        
        quantity = int(quantity)
        price = float(price)
        total = quantity * price
        user_id = session.get('user_id', 1)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT,
                quantity INTEGER,
                buy_price REAL,
                total REAL,
                buy_date TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO stock_portfolio (user_id, symbol, quantity, buy_price, total, buy_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, symbol, quantity, price, total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        conn.close()
        
        print(f"✅ BOUGHT: {quantity} {symbol} @ ₹{price}")
        print("="*50)
        
        return jsonify({
            'success': True,
            'message': f'Bought {quantity} shares of {symbol} at ₹{price}',
            'total': total
        })
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
@market_live_bp.route('/sell', methods=['POST'])
def sell_stock():
    print("\n" + "="*50)
    print("🔴 SELL ROUTE HIT")
    
    try:
        data = request.get_json()
        print(f"Data: {data}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No data'}), 400
        
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        price = data.get('price')
        
        quantity = int(quantity)
        price = float(price)
        total = quantity * price
        user_id = session.get('user_id', 1)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check holdings
        cursor.execute('SELECT SUM(quantity) FROM stock_portfolio WHERE user_id = ? AND symbol = ?', (user_id, symbol))
        result = cursor.fetchone()
        owned = result[0] if result[0] else 0
        
        if owned < quantity:
            conn.close()
            return jsonify({'success': False, 'error': f'Only {owned} shares available'}), 400
        
        # Create sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT,
                quantity INTEGER,
                sell_price REAL,
                total REAL,
                sell_date TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO stock_sales (user_id, symbol, quantity, sell_price, total, sell_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, symbol, quantity, price, total, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # FIFO removal
        cursor.execute('SELECT id, quantity FROM stock_portfolio WHERE user_id = ? AND symbol = ? ORDER BY id ASC', (user_id, symbol))
        purchases = cursor.fetchall()
        remaining = quantity
        
        for pid, qty in purchases:
            if remaining <= 0:
                break
            if qty <= remaining:
                cursor.execute('DELETE FROM stock_portfolio WHERE id = ?', (pid,))
                remaining -= qty
            else:
                cursor.execute('UPDATE stock_portfolio SET quantity = ? WHERE id = ?', (qty - remaining, pid))
                remaining = 0
        
        conn.commit()
        conn.close()
        
        print(f"✅ SOLD: {quantity} {symbol} @ ₹{price}")
        print("="*50)
        
        return jsonify({
            'success': True,
            'message': f'Sold {quantity} shares of {symbol} at ₹{price}',
            'total': total
        })
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
@market_live_bp.route('/portfolio')
def portfolio():
    user_id = session.get('user_id', 1)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT symbol, SUM(quantity) as qty, SUM(total) as invested
        FROM stock_portfolio
        WHERE user_id = ?
        GROUP BY symbol
    ''', (user_id,))
    purchases = cursor.fetchall()
    
    cursor.execute('''
        SELECT symbol, SUM(quantity) as sold
        FROM stock_sales
        WHERE user_id = ?
        GROUP BY symbol
    ''', (user_id,))
    sales = cursor.fetchall()
    
    conn.close()
    
    holdings = {}
    for p in purchases:
        holdings[p[0]] = {'qty': p[1], 'invested': p[2]}
    
    for s in sales:
        if s[0] in holdings:
            holdings[s[0]]['qty'] -= s[1]
    
    result = []
    for symbol, data in holdings.items():
        if data['qty'] > 0:
            result.append({
                'symbol': symbol,
                'quantity': data['qty'],
                'invested': round(data['invested'], 2),
                'current_price': get_live_price(symbol)
            })
    
    return render_template('market_live/portfolio.html', stocks=result)