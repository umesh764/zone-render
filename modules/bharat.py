from flask import Blueprint, render_template, request, jsonify
from modules.models import db, BharatDarshan
from sqlalchemy import or_

bharat_bp = Blueprint('bharat', __name__, url_prefix='/bharat')

@bharat_bp.route('/')
def home():
    """भारत दर्शन का होम पेज"""
    featured = BharatDarshan.query.limit(6).all()
    
    # Distinct states and categories
    states = db.session.query(BharatDarshan.state).distinct().all()
    categories = db.session.query(BharatDarshan.category).distinct().all()
    
    return render_template('bharat/home.html',
                         featured=featured,
                         states=[s[0] for s in states if s[0]],
                         categories=[c[0] for c in categories if c[0]])

@bharat_bp.route('/state/<string:state_name>')
def state_view(state_name):
    """राज्य के अनुसार देखें"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(state=state_name).order_by(BharatDarshan.name).paginate(page=page, per_page=12)
    return render_template('bharat/state.html',
                         items=items,
                         state=state_name)

@bharat_bp.route('/category/<string:category_name>')
def category_view(category_name):
    """श्रेणी के अनुसार देखें"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(category=category_name).order_by(BharatDarshan.name).paginate(page=page, per_page=12)
    return render_template('bharat/category.html',
                         items=items,
                         category=category_name)

@bharat_bp.route('/item/<int:item_id>')
def item_detail(item_id):
    """किसी एक आइटम का विस्तृत पेज"""
    item = BharatDarshan.query.get_or_404(item_id)
    return render_template('bharat/detail.html', item=item)

@bharat_bp.route('/search')
def search():
    """खोज फंक्शन"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    results = BharatDarshan.query.filter(
        or_(
            BharatDarshan.name.ilike(f'%{query}%'),
            BharatDarshan.name_hindi.ilike(f'%{query}%'),
            BharatDarshan.description.ilike(f'%{query}%'),
            BharatDarshan.state.ilike(f'%{query}%'),
            BharatDarshan.city.ilike(f'%{query}%'),
            BharatDarshan.district.ilike(f'%{query}%'),
            BharatDarshan.category.ilike(f'%{query}%'),
            BharatDarshan.subcategory.ilike(f'%{query}%'),
            BharatDarshan.cuisine.ilike(f'%{query}%'),
            BharatDarshan.famous_food.ilike(f'%{query}%'),
            BharatDarshan.dress_code.ilike(f'%{query}%'),
            BharatDarshan.cultural_facts.ilike(f'%{query}%'),
            BharatDarshan.famous_markets.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'name_hindi': r.name_hindi,
        'category': r.category,
        'subcategory': r.subcategory,
        'state': r.state,
        'city': r.city,
        'district': r.district,
        'main_image': r.main_image,
        'description': r.description[:100] + '...' if r.description else ''
    } for r in results])

@bharat_bp.route('/district/<string:district_name>')
def district_view(district_name):
    """जिला के अनुसार देखें"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(district=district_name).order_by(BharatDarshan.name).paginate(page=page, per_page=12)
    return render_template('bharat/district.html',
                         items=items,
                         district=district_name)

@bharat_bp.route('/city/<string:city_name>')
def city_view(city_name):
    """शहर के अनुसार देखें"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(city=city_name).order_by(BharatDarshan.name).paginate(page=page, per_page=12)
    return render_template('bharat/city.html',
                         items=items,
                         city=city_name)

@bharat_bp.route('/festivals')
def festivals():
    """सभी त्योहार"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(category='त्योहार').order_by(BharatDarshan.festival_month).paginate(page=page, per_page=12)
    return render_template('bharat/festivals.html', items=items)

@bharat_bp.route('/markets')
def markets():
    """सभी बाज़ार"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(category='बाज़ार').order_by(BharatDarshan.name).paginate(page=page, per_page=12)
    return render_template('bharat/markets.html', items=items)

@bharat_bp.route('/food')
def food():
    """सभी व्यंजन"""
    page = request.args.get('page', 1, type=int)
    items = BharatDarshan.query.filter_by(category='भोजन').order_by(BharatDarshan.name).paginate(page=page, per_page=12)
    return render_template('bharat/food.html', items=items)