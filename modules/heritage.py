from flask import Blueprint, render_template, request, jsonify
from modules.models import db, HeritageSite
from sqlalchemy import or_

heritage_bp = Blueprint('heritage', __name__, url_prefix='/heritage')

# मुख्य श्रेणियाँ
CATEGORIES = ['मंदिर', 'किला', 'स्मारक', 'गुफा', 'मस्जिद', 'गुरुद्वारा', 'चर्च', 'स्तूप', 'महल']
STATES = [
    'उत्तर प्रदेश', 'मध्य प्रदेश', 'राजस्थान', 'गुजरात', 'महाराष्ट्र', 
    'कर्नाटक', 'तमिलनाडु', 'केरल', 'आंध्र प्रदेश', 'तेलंगाना',
    'उड़ीसा', 'पश्चिम बंगाल', 'बिहार', 'झारखंड', 'असम', 'हिमाचल प्रदेश',
    'उत्तराखंड', 'जम्मू और कश्मीर', 'लद्दाख', 'दिल्ली'
]

@heritage_bp.route('/')
def home():
    """भारत दर्शन का होम पेज"""
    # सारी एक्टिव sites लाओ (बिना limit के)
    all_sites = HeritageSite.query.filter_by(is_active=True).all()
    
    # पहली 6 sites featured के लिए
    featured = all_sites[:6] if len(all_sites) > 6 else all_sites
    
    # डीबग प्रिंट (CMD में दिखेगा)
    print(f"\n=== HERITAGE HOME PAGE ===")
    print(f"Total active sites: {len(all_sites)}")
    print(f"Featured sites: {len(featured)}")
    print("=" * 30)
    
    return render_template('heritage/home.html',
                         sites=all_sites,        # यह नई लाइन - सारी sites
                         featured=featured,       # यह पुरानी लाइन - पहली 6 sites
                         categories=CATEGORIES,
                         states=STATES)    
    if not query and not category and not state:
        return jsonify([])
    
    filters = [HeritageSite.is_active == True]
    
    if query:
        filters.append(
            or_(
                HeritageSite.name.ilike(f'%{query}%'),
                HeritageSite.name_hindi.ilike(f'%{query}%'),
                HeritageSite.description.ilike(f'%{query}%'),
                HeritageSite.history.ilike(f'%{query}%'),
                HeritageSite.tags.ilike(f'%{query}%'),
                HeritageSite.location.ilike(f'%{query}%')
            )
        )
    
    if category:
        filters.append(HeritageSite.category == category)
    
    if state:
        filters.append(HeritageSite.state == state)
    
    results = HeritageSite.query.filter(*filters).limit(50).all()
    
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'name_hindi': s.name_hindi,
        'category': s.category,
        'state': s.state,
        'description': s.description[:200] + '...' if s.description else '',
        'image_url': s.image_url,
        'built_year': s.built_year
    } for s in results])

@heritage_bp.route('/site/<int:site_id>')
def site_detail(site_id):
    """किसी एक स्थल का विस्तृत पेज"""
    site = HeritageSite.query.get_or_404(site_id)
    return render_template('heritage/site_detail.html', site=site)

@heritage_bp.route('/category/<string:category_name>')
def category_view(category_name):
    """श्रेणी के अनुसार स्थल"""
    page = request.args.get('page', 1, type=int)
    sites = HeritageSite.query.filter_by(category=category_name, is_active=True).paginate(page=page, per_page=12)
    return render_template('heritage/category.html',
                         sites=sites,
                         category=category_name,
                         title=f"{category_name} - भारत दर्शन")

@heritage_bp.route('/state/<string:state_name>')
def state_view(state_name):
    """राज्य के अनुसार स्थल"""
    page = request.args.get('page', 1, type=int)
    sites = HeritageSite.query.filter_by(state=state_name, is_active=True).paginate(page=page, per_page=12)
    return render_template('heritage/state.html',
                         sites=sites,
                         state=state_name,
                         title=f"{state_name} के धरोहर स्थल")

@heritage_bp.route('/map')
def heritage_map():
    """धरोहर स्थलों का नक्शा"""
    sites = HeritageSite.query.filter_by(is_active=True).all()
    return render_template('heritage/map.html', sites=sites)