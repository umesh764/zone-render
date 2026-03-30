from flask import Blueprint, render_template, jsonify, request, session
import json
import os
from datetime import datetime

simple_market_bp = Blueprint('simple_market', __name__, url_prefix='/simple-market')

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'zone.db')

# Stock data (offline ready)
STOCKS = [
    {'symbol': 'RELIANCE', 'name': 'Reliance Industries', 'price': 2500},
    {'symbol': 'TCS', 'name': 'Tata Consultancy', 'price': 3800},
    {'symbol': 'HDFCBANK', 'name': 'HDFC Bank', 'price': 1600},
    {'symbol': 'INFY', 'name': 'Infosys', 'price': 1400},
    {'symbol': 'ICICIBANK', 'name': 'ICICI Bank', 'price': 1100},
    {'symbol': 'TATAMOTORS', 'name': 'Tata Motors', 'price': 980},
    {'symbol': 'SBIN', 'name': 'State Bank of India', 'price': 700},
    {'symbol': 'BHARTIARTL', 'name': 'Bharti Airtel', 'price': 1500},
    {'symbol': 'ITC', 'name': 'ITC Limited', 'price': 450},
    {'symbol': 'NTPC', 'name': 'NTPC Limited', 'price': 350}
]

@simple_market_bp.route('/')
def dashboard():
    """Main market dashboard"""
    return render_template('simple_market/dashboard.html', stocks=STOCKS)

@simple_market_bp.route('/api/stocks')
def api_stocks():
    """Get all stocks with current prices"""
    return jsonify(STOCKS)

@simple_market_bp.route('/buy', methods=['POST'])
def buy_stock():
    """Buy stocks - works offline"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400
        
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        price = data.get('price')
        
        if not symbol or not quantity or not price:
            return jsonify({'success': False, 'error': 'Missing fields'}), 400
        
        quantity = int(quantity)
        price = float(price)
        
        if quantity <= 0 or price <= 0:
            return jsonify({'success': False, 'error': 'Invalid values'}), 400
        
        total = quantity * price
        user_id = session.get('user_id', 1)
        
        # Save to database (offline friendly)
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simple_portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT,
                quantity INTEGER,
                avg_price REAL,
                total_invested REAL,
                purchase_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simple_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT,
                type TEXT,
                quantity INTEGER,
                price REAL,
                total REAL,
                transaction_date TEXT
            )
        ''')
        
        # Check if already in portfolio
        cursor.execute('SELECT quantity, avg_price FROM simple_portfolio WHERE user_id = ? AND symbol = ?', 
                      (user_id, symbol))
        existing = cursor.fetchone()
        
        if existing:
            old_qty = existing[0]
            old_avg = existing[1]
            new_qty = old_qty + quantity
            new_avg = ((old_qty * old_avg) + (quantity * price)) / new_qty
            
            cursor.execute('''
                UPDATE simple_portfolio 
                SET quantity = ?, avg_price = ?, total_invested = total_invested + ?
                WHERE user_id = ? AND symbol = ?
            ''', (new_qty, new_avg, total, user_id, symbol))
        else:
            cursor.execute('''
                INSERT INTO simple_portfolio (user_id, symbol, quantity, avg_price, total_invested, purchase_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, symbol, quantity, price, total, datetime.now().isoformat()))
        
        # Record transaction
        cursor.execute('''
            INSERT INTO simple_transactions (user_id, symbol, type, quantity, price, total, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, symbol, 'BUY', quantity, price, total, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ BOUGHT: {quantity} {symbol} @ ₹{price} = ₹{total}")
        
        return jsonify({
            'success': True,
            'message': f'Bought {quantity} shares of {symbol} at ₹{price}',
            'total': total
        })
        
    except Exception as e:
        print(f"❌ Buy error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@simple_market_bp.route('/sell', methods=['POST'])
def sell_stock():
    """Sell stocks - works offline"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400
        
        symbol = data.get('symbol')
        quantity = data.get('quantity')
        price = data.get('price')
        
        if not symbol or not quantity or not price:
            return jsonify({'success': False, 'error': 'Missing fields'}), 400
        
        quantity = int(quantity)
        price = float(price)
        
        if quantity <= 0 or price <= 0:
            return jsonify({'success': False, 'error': 'Invalid values'}), 400
        
        total = quantity * price
        user_id = session.get('user_id', 1)
        
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check portfolio
        cursor.execute('SELECT quantity FROM simple_portfolio WHERE user_id = ? AND symbol = ?', 
                      (user_id, symbol))
        existing = cursor.fetchone()
        
        if not existing:
            return jsonify({'success': False, 'error': 'Stock not in portfolio'}), 400
        
        if existing[0] < quantity:
            return jsonify({'success': False, 'error': 'Not enough shares'}), 400
        
        new_qty = existing[0] - quantity
        
        if new_qty == 0:
            cursor.execute('DELETE FROM simple_portfolio WHERE user_id = ? AND symbol = ?', 
                          (user_id, symbol))
        else:
            cursor.execute('''
                UPDATE simple_portfolio 
                SET quantity = ?
                WHERE user_id = ? AND symbol = ?
            ''', (new_qty, user_id, symbol))
        
        # Record transaction
        cursor.execute('''
            INSERT INTO simple_transactions (user_id, symbol, type, quantity, price, total, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, symbol, 'SELL', quantity, price, total, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"✅ SOLD: {quantity} {symbol} @ ₹{price} = ₹{total}")
        
        return jsonify({
            'success': True,
            'message': f'Sold {quantity} shares of {symbol} at ₹{price}',
            'total': total
        })
        
    except Exception as e:
        print(f"❌ Sell error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@simple_market_bp.route('/portfolio')
def portfolio():
    """View portfolio"""
    user_id = session.get('user_id', 1)
    
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT symbol, quantity, avg_price, total_invested FROM simple_portfolio 
        WHERE user_id = ?
    ''', (user_id,))
    
    portfolio_items = cursor.fetchall()
    conn.close()
    
    portfolio_data = []
    total_value = 0
    total_invested = 0
    
    for item in portfolio_items:
        symbol = item[0]
        quantity = item[1]
        avg_price = item[2]
        invested = item[3]
        
        # Get current price
        current_price = next((s['price'] for s in STOCKS if s['symbol'] == symbol), avg_price)
        current_value = quantity * current_price
        profit_loss = current_value - invested
        profit_loss_percent = (profit_loss / invested) * 100 if invested > 0 else 0
        
        portfolio_data.append({
            'symbol': symbol,
            'quantity': quantity,
            'avg_price': avg_price,
            'invested': invested,
            'current_price': current_price,
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percent': profit_loss_percent
        })
        
        total_value += current_value
        total_invested += invested
    
    return render_template('simple_market/portfolio.html',
                         portfolio=portfolio_data,
                         total_value=total_value,
                         total_invested=total_invested,
                         total_profit_loss=total_value - total_invested)