from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import or_
import json

gov_bp = Blueprint('gov', __name__, url_prefix='/gov')

# State details dictionary
STATE_DETAILS = {
    'उत्तर प्रदेश': {
        'capital': 'लखनऊ',
        'language': 'हिंदी',
        'culture': {
            'dress': 'पुरुष: धोती-कुर्ता, महिला: साड़ी-सलवार कमीज',
            'food': ['टुंडे कबाब', 'बिरयानी', 'चाट', 'पेठा'],
            'festivals': ['दीपावली', 'होली', 'रामलीला', 'ताज महोत्सव']
        },
        'famous_places': [
            {'name': 'ताज महल', 'type': 'ऐतिहासिक'},
            {'name': 'वाराणसी घाट', 'type': 'धार्मिक'},
            {'name': 'फतेहपुर सीकरी', 'type': 'ऐतिहासिक'}
        ]
    },
    'महाराष्ट्र': {
        'capital': 'मुंबई',
        'language': 'मराठी',
        'culture': {
            'dress': 'पुरुष: धोती-कुर्ता, महिला: नववरी साड़ी',
            'food': ['वड़ा पाव', 'पाव भाजी', 'पुरण पोळी'],
            'festivals': ['गणेश चतुर्थी', 'गुढी पाडवा']
        },
        'famous_places': [
            {'name': 'गेटवे ऑफ इंडिया', 'type': 'ऐतिहासिक'},
            {'name': 'अजंता-एलोरा गुफाएं', 'type': 'ऐतिहासिक'},
            {'name': 'शिरडी साईं बाबा', 'type': 'धार्मिक'}
        ]
    },
    'दिल्ली': {
        'capital': 'नई दिल्ली',
        'language': 'हिंदी, पंजाबी',
        'culture': {
            'dress': 'आधुनिक एवं पारंपरिक',
            'food': ['छोले भटूरे', 'बटर चिकन', 'परांठे'],
            'festivals': ['दीपावली', 'होली', 'गणतंत्र दिवस']
        },
        'famous_places': [
            {'name': 'लाल किला', 'type': 'ऐतिहासिक'},
            {'name': 'इंडिया गेट', 'type': 'राष्ट्रीय'},
            {'name': 'कुतुब मीनार', 'type': 'ऐतिहासिक'}
        ]
    },
    'कर्नाटक': {
        'capital': 'बेंगलुरु',
        'language': 'कन्नड़',
        'culture': {
            'dress': 'पुरुष: पंचे, महिला: सीरे',
            'food': ['बिसिबेले भात', 'मैसूर पाक', 'दोसा'],
            'festivals': ['मैसूर दसरा', 'उगादि']
        },
        'famous_places': [
            {'name': 'मैसूर पैलेस', 'type': 'ऐतिहासिक'},
            {'name': 'हम्पी', 'type': 'पुरातात्विक'},
            {'name': 'कूर्ग', 'type': 'हिल स्टेशन'}
        ]
    },
    'तमिलनाडु': {
        'capital': 'चेन्नई',
        'language': 'तमिल',
        'culture': {
            'dress': 'पुरुष: वेष्टि, महिला: साड़ी',
            'food': ['इडली', 'डोसा', 'पोंगल'],
            'festivals': ['पोंगल', 'तमिल नववर्ष']
        },
        'famous_places': [
            {'name': 'मीनाक्षी मंदिर', 'type': 'धार्मिक'},
            {'name': 'मामल्लापुरम', 'type': 'ऐतिहासिक'},
            {'name': 'ऊटी', 'type': 'हिल स्टेशन'}
        ]
    },
    'राजस्थान': {
        'capital': 'जयपुर',
        'language': 'राजस्थानी',
        'culture': {
            'dress': 'पुरुष: पगड़ी-धोती, महिला: घाघरा-चोली',
            'food': ['दाल बाटी चूरमा', 'गट्टे की सब्जी'],
            'festivals': ['पुष्कर मेला', 'गणगौर']
        },
        'famous_places': [
            {'name': 'हवा महल', 'type': 'ऐतिहासिक'},
            {'name': 'उदयपुर सिटी पैलेस', 'type': 'शाही'},
            {'name': 'जैसलमेर किला', 'type': 'किला'}
        ]
    }
}

def get_state_details(state_name):
    """Get state details"""
    return STATE_DETAILS.get(state_name, None)

@gov_bp.route('/')
def home():
    """Government services home page"""
    try:
        categories = ['Passport', 'Driving License', 'PAN', 'Aadhaar', 'Voter ID', 
                     'Birth Certificate', 'Marriage Certificate', 'Income Certificate']
        states = list(STATE_DETAILS.keys())
        
        return render_template('gov/home.html', 
                             categories=categories, 
                             states=states)
    except Exception as e:
        print(f"Error in gov home: {e}")
        return render_template('gov/home.html', 
                             categories=['Passport', 'Driving License', 'PAN', 'Aadhaar'],
                             states=['उत्तर प्रदेश', 'महाराष्ट्र', 'दिल्ली'])

@gov_bp.route('/services')
def all_services():
    """All government services"""
    try:
        services_list = [
            'Passport Services', 'Driving License', 'PAN Card', 'Aadhaar', 'Voter ID',
            'Birth Certificate', 'Marriage Certificate', 'Income Certificate', 'Caste Certificate',
            'Domicile Certificate', 'Electricity Bill Payment', 'Water Bill Payment', 'Property Tax'
        ]
        total = len(services_list)
        
        return render_template('gov/services.html', 
                             categories=services_list,
                             total_services=total)
    except Exception as e:
        print(f"Error in services: {e}")
        return render_template('gov/services.html', 
                             categories=['Passport', 'Driving License', 'PAN', 'Aadhaar'],
                             total_services=4)

@gov_bp.route('/service/<string:service_name>')
def service_detail(service_name):
    """Service detail page"""
    try:
        service = {
            'name': service_name,
            'description': f'{service_name} सेवा के लिए ऑनलाइन आवेदन करें। यह सेवा नागरिकों को सुविधा प्रदान करती है।',
            'fees': 100,
            'processing_time': '15-30 दिन',
            'documents': ['आधार कार्ड', 'पैन कार्ड', 'पासपोर्ट साइज फोटो', 'पता प्रमाण'],
            'eligibility': 'भारतीय नागरिक',
            'application_mode': 'ऑनलाइन एवं ऑफलाइन',
            'website': 'https://services.india.gov.in'
        }
        
        return render_template('gov/service_detail.html', 
                             service_name=service_name, 
                             service=service)
    except Exception as e:
        print(f"Error in service detail: {e}")
        return render_template('gov/service_detail.html', 
                             service_name=service_name, 
                             service={'name': service_name, 'description': 'Service details coming soon'})

@gov_bp.route('/state/<string:state_name>')
def state_view(state_name):
    """State dashboard"""
    try:
        state_details = get_state_details(state_name)
        
        # Sample departments data
        departments = [
            {'name': 'जिला कलेक्टर कार्यालय', 'category': 'प्रशासन', 'status': 'active'},
            {'name': 'पुलिस अधीक्षक कार्यालय', 'category': 'पुलिस', 'status': 'active'},
            {'name': 'नगर निगम', 'category': 'नगरीय निकाय', 'status': 'active'},
            {'name': 'आयुर्वेद विभाग', 'category': 'स्वास्थ्य', 'status': 'active'}
        ]
        
        state_stats = {
            'name': state_name,
            'total_depts': len(departments),
            'categories': 4
        }
        
        return render_template('gov/state_dashboard.html', 
                             departments={'items': departments, 'total': len(departments)},
                             state=state_stats,
                             details=state_details)
    except Exception as e:
        print(f"Error in state view: {e}")
        return render_template('gov/state.html', state_name=state_name)

@gov_bp.route('/category/<string:category_name>')
def category_view(category_name):
    """Category wise services"""
    try:
        services = [
            {'name': f'{category_name} Application', 'description': 'नया आवेदन', 'fees': 100, 'status': 'active'},
            {'name': f'{category_name} Renewal', 'description': 'नवीनीकरण', 'fees': 50, 'status': 'active'},
            {'name': f'{category_name} Correction', 'description': 'सुधार', 'fees': 75, 'status': 'active'},
            {'name': f'{category_name} Duplicate', 'description': 'डुप्लीकेट', 'fees': 60, 'status': 'active'}
        ]
        
        return render_template('gov/category.html', 
                             departments={'items': services, 'total': len(services)},
                             category_name=category_name)
    except Exception as e:
        print(f"Error in category view: {e}")
        return render_template('gov/category.html', 
                             departments={'items': [], 'total': 0},
                             category_name=category_name)

@gov_bp.route('/department/<string:dept_name>')
def department_detail(dept_name):
    """Department details"""
    try:
        department = {
            'name': dept_name,
            'description': f'{dept_name} विभाग नागरिकों को विभिन्न सेवाएं प्रदान करता है।',
            'services': ['सेवा 1', 'सेवा 2', 'सेवा 3'],
            'contact': '1800-XXX-XXXX',
            'email': f'{dept_name.lower()}@gov.in',
            'website': f'https://{dept_name.lower()}.gov.in',
            'address': 'मुख्यालय, नई दिल्ली'
        }
        
        return render_template('gov/department.html', 
                             department=department,
                             dept_name=dept_name)
    except Exception as e:
        print(f"Error in department detail: {e}")
        return render_template('gov/department.html', 
                             department={'name': dept_name, 'description': 'Details coming soon'},
                             dept_name=dept_name)

@gov_bp.route('/direct-services')
def direct_services():
    """Direct services portal"""
    try:
        services_list = [
            {'name': 'Passport Seva', 'url': '/gov/service/Passport', 'icon': 'passport', 'description': 'पासपोर्ट आवेदन और नवीनीकरण'},
            {'name': 'Driving License', 'url': '/gov/service/Driving License', 'icon': 'driving', 'description': 'लर्नर और पक्का लाइसेंस'},
            {'name': 'PAN Card', 'url': '/gov/service/PAN Card', 'icon': 'pan', 'description': 'नया पैन और सुधार'},
            {'name': 'Aadhaar', 'url': '/gov/service/Aadhaar', 'icon': 'aadhaar', 'description': 'आधार एनरोलमेंट और अपडेट'},
            {'name': 'Voter ID', 'url': '/gov/service/Voter ID', 'icon': 'voter', 'description': 'मतदाता पहचान पत्र'},
            {'name': 'Birth Certificate', 'url': '/gov/service/Birth Certificate', 'icon': 'birth', 'description': 'जन्म प्रमाण पत्र'}
        ]
        
        return render_template('gov/direct_services.html', services=services_list)
    except Exception as e:
        print(f"Error in direct services: {e}")
        return render_template('gov/direct_services.html', services=[])

@gov_bp.route('/companies')
def companies():
    """Government companies and PSUs"""
    try:
        companies_list = [
            {'name': 'BHEL', 'sector': 'Heavy Engineering', 'website': 'bhel.com', 'status': 'active'},
            {'name': 'SAIL', 'sector': 'Steel', 'website': 'sail.co.in', 'status': 'active'},
            {'name': 'ONGC', 'sector': 'Oil & Gas', 'website': 'ongcindia.com', 'status': 'active'},
            {'name': 'NTPC', 'sector': 'Power', 'website': 'ntpc.co.in', 'status': 'active'},
            {'name': 'IOCL', 'sector': 'Petroleum', 'website': 'iocl.com', 'status': 'active'},
            {'name': 'BPCL', 'sector': 'Petroleum', 'website': 'bharatpetroleum.in', 'status': 'active'},
            {'name': 'HPCL', 'sector': 'Petroleum', 'website': 'hpcl.com', 'status': 'active'}
        ]
        
        return render_template('gov/companies.html', companies=companies_list)
    except Exception as e:
        print(f"Error in companies: {e}")
        return render_template('gov/companies.html', companies=[])

@gov_bp.route('/all-states')
def all_states():
    """All states information"""
    try:
        states = list(STATE_DETAILS.keys())
        return render_template('gov/all_states.html', states=states)
    except Exception as e:
        print(f"Error in all states: {e}")
        return render_template('gov/all_states.html', states=[])

@gov_bp.route('/search')
def search():
    """Search endpoint"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify([])
        
        # Simple search in state details
        results = []
        for state_name, state_data in STATE_DETAILS.items():
            if query.lower() in state_name.lower():
                results.append({
                    'id': state_name,
                    'name': state_name,
                    'category': 'State',
                    'description': state_data.get('capital', '')
                })
        
        # Add sample service results
        services = ['Passport', 'Driving License', 'PAN Card', 'Aadhaar', 'Voter ID']
        for service in services:
            if query.lower() in service.lower():
                results.append({
                    'id': service,
                    'name': service,
                    'category': 'Service',
                    'description': f'{service} सेवा के लिए आवेदन करें'
                })
        
        return jsonify(results[:10])
    except Exception as e:
        print(f"Error in search: {e}")
        return jsonify([])

@gov_bp.route('/district/<string:state_name>/<string:district_name>')
def district_detail(state_name, district_name):
    """District detail page"""
    try:
        district_info = {
            'headquarters': district_name,
            'population': '5,00,000',
            'area': '5,000',
            'literacy_rate': '85%',
            'tehsils': '10',
            'dm_contact': '1800-XXX-XXXX',
            'sp_contact': '1800-XXX-XXXX',
            'hospital_contact': '1800-XXX-XXXX',
            'helpline': '100',
            'gov_offices': [
                {'name': 'जिला कलेक्टर कार्यालय', 'url': '#'},
                {'name': 'पुलिस अधीक्षक कार्यालय', 'url': '#'}
            ],
            'local_services': [
                {'name': 'आधार केंद्र', 'url': '#'},
                {'name': 'पासपोर्ट कार्यालय', 'url': '#'}
            ]
        }
        
        return render_template('gov/districts/district_detail.html',
                             district_name=district_name,
                             state_name=state_name,
                             district_headquarters=district_info['headquarters'],
                             population=district_info['population'],
                             area=district_info['area'],
                             literacy_rate=district_info['literacy_rate'],
                             tehsils=district_info['tehsils'],
                             dm_contact=district_info['dm_contact'],
                             sp_contact=district_info['sp_contact'],
                             hospital_contact=district_info['hospital_contact'],
                             helpline=district_info['helpline'],
                             gov_offices=district_info['gov_offices'],
                             local_services=district_info['local_services'])
    except Exception as e:
        print(f"Error in district detail: {e}")
        return f"<h1>{district_name} जिला</h1><p>District details coming soon</p>"