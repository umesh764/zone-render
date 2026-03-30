from flask import Blueprint, render_template, request, jsonify
from modules.models import db, GovernmentDepartment
from modules.gov_services import GovernmentServices
from sqlalchemy import or_

gov_bp = Blueprint('gov', __name__, url_prefix='/gov')

# सभी राज्यों का डेटा एक साथ
STATE_DETAILS = {
    # उत्तर भारत
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
        ],
        'markets': [
            {'name': 'चौक बाजार', 'city': 'लखनऊ', 'specialty': 'चिकनकारी'},
            {'name': 'सदर बाजार', 'city': 'आगरा', 'specialty': 'संगमरमर'}
        ]
    },
    'पंजाब': {
        'capital': 'चंडीगढ़',
        'language': 'पंजाबी',
        'culture': {
            'dress': 'पुरुष: पगड़ी-कुर्ता, महिला: पटियाला सूट',
            'food': ['मक्की दी रोटी', 'सरसों दा साग', 'माखन', 'लस्सी'],
            'festivals': ['बैसाखी', 'लोहड़ी', 'गुरुपर्व']
        },
        'famous_places': [
            {'name': 'स्वर्ण मंदिर', 'type': 'धार्मिक'},
            {'name': 'जलियांवाला बाग', 'type': 'ऐतिहासिक'},
            {'name': 'वाघा बॉर्डर', 'type': 'राष्ट्रीय'}
        ],
        'markets': [
            {'name': 'सदर बाजार', 'city': 'अमृतसर', 'specialty': 'जूते'},
            {'name': 'एलांटे मॉल', 'city': 'चंडीगढ़', 'specialty': 'ब्रांडेड'}
        ]
    },
    'हरियाणा': {
        'capital': 'चंडीगढ़',
        'language': 'हरियाणवी',
        'culture': {
            'dress': 'पुरुष: धोती-कुर्ता, महिला: दमण-साड़ी',
            'food': ['बाजरे की रोटी', 'खिचड़ी', 'चूरमा', 'कढ़ी'],
            'festivals': ['होली', 'गुग्गा नवमी', 'तीज']
        },
        'famous_places': [
            {'name': 'कुरुक्षेत्र', 'type': 'धार्मिक'},
            {'name': 'सुल्तानपुर झील', 'type': 'प्राकृतिक'},
            {'name': 'साइबर सिटी', 'type': 'आधुनिक'}
        ],
        'markets': [
            {'name': 'साइबर हब', 'city': 'गुरुग्राम', 'specialty': 'रेस्टोरेंट्स'},
            {'name': 'शॉपिंग मॉल', 'city': 'फरीदाबाद', 'specialty': 'फैशन'}
        ]
    },
    'राजस्थान': {
        'capital': 'जयपुर',
        'language': 'राजस्थानी, हिंदी',
        'culture': {
            'dress': 'पुरुष: पगड़ी-धोती, महिला: घाघरा-चोली',
            'food': ['दाल बाटी चूरमा', 'गट्टे की सब्जी', 'कढ़ी', 'मावा कचोरी'],
            'festivals': ['तेजा दशमी', 'गणगौर', 'पुष्कर मेला']
        },
        'famous_places': [
            {'name': 'हवा महल', 'type': 'ऐतिहासिक'},
            {'name': 'उदयपुर सिटी पैलेस', 'type': 'शाही'},
            {'name': 'जैसलमेर किला', 'type': 'किला'}
        ],
        'markets': [
            {'name': 'जौहरी बाजार', 'city': 'जयपुर', 'specialty': 'ज्वैलरी'},
            {'name': 'बापू बाजार', 'city': 'जयपुर', 'specialty': 'टेक्सटाइल'}
        ]
    },
    'हिमाचल प्रदेश': {
        'capital': 'शिमला',
        'language': 'पहाड़ी, हिंदी',
        'culture': {
            'dress': 'पुरुष: चोला-पायजामा, महिला: पछरा',
            'food': ['सिद्दू', 'बाबरू', 'चना मडरा', 'मधरा'],
            'festivals': ['शूलिनी मेला', 'मिंजर मेला', 'दशहरा']
        },
        'famous_places': [
            {'name': 'मनाली', 'type': 'हिल स्टेशन'},
            {'name': 'धर्मशाला', 'type': 'बौद्ध संस्कृति'},
            {'name': 'खज्जियार', 'type': 'हिल स्टेशन'}
        ],
        'markets': [
            {'name': 'माल रोड', 'city': 'शिमला', 'specialty': 'हस्तशिल्प'},
            {'name': 'इब्बा बाजार', 'city': 'मनाली', 'specialty': 'ऊनी कपड़े'}
        ]
    },
    'उत्तराखंड': {
        'capital': 'देहरादून',
        'language': 'गढ़वाली, कुमाऊँनी',
        'culture': {
            'dress': 'पुरुष: पिछौड़ा, महिला: घाघरा',
            'food': ['फांणू', 'कापा', 'झंगोरे की खीर', 'बाड़ी'],
            'festivals': ['गंगा दशहरा', 'केदारनाथ यात्रा', 'फूलदेई']
        },
        'famous_places': [
            {'name': 'नैनीताल', 'type': 'हिल स्टेशन'},
            {'name': 'ऋषिकेश', 'type': 'धार्मिक'},
            {'name': 'जिम कॉर्बेट', 'type': 'राष्ट्रीय उद्यान'}
        ],
        'markets': [
            {'name': 'पलटन बाजार', 'city': 'देहरादून', 'specialty': 'ऊनी वस्त्र'},
            {'name': 'लैंसडाउन बाजार', 'city': 'लैंसडाउन', 'specialty': 'आयुर्वेदिक'}
        ]
    },
    'जम्मू और कश्मीर': {
        'capital': 'श्रीनगर (गर्मी), जम्मू (सर्दी)',
        'language': 'कश्मीरी, डोगरी, उर्दू',
        'culture': {
            'dress': 'पुरुष: फेरन, महिला: फेरन',
            'food': ['रोगन जोश', 'गुश्ताबा', 'दम आलू', 'नोन चाय'],
            'festivals': ['ईद', 'लोसार', 'हरि रब्बा']
        },
        'famous_places': [
            {'name': 'डल झील', 'type': 'प्राकृतिक'},
            {'name': 'गुलमर्ग', 'type': 'हिल स्टेशन'},
            {'name': 'वैष्णो देवी', 'type': 'धार्मिक'}
        ],
        'markets': [
            {'name': 'लाल चौक', 'city': 'श्रीनगर', 'specialty': 'हस्तशिल्प'},
            {'name': 'रघुनाथ बाजार', 'city': 'जम्मू', 'specialty': 'डोगरी चप्पलें'}
        ]
    },
    'दिल्ली': {
        'capital': 'नई दिल्ली',
        'language': 'हिंदी, पंजाबी, उर्दू',
        'culture': {
            'dress': 'पुरुष: कुर्ता-पायजामा, महिला: सलवार-सूट, साड़ी',
            'food': ['छोले-भटूरे', 'परांठा', 'चाट', 'बटर चिकन'],
            'festivals': ['दिवाली', 'दुर्गा पूजा', 'लोहड़ी', 'ईद']
        },
        'famous_places': [
            {'name': 'लाल किला', 'type': 'ऐतिहासिक'},
            {'name': 'इंडिया गेट', 'type': 'राष्ट्रीय स्मारक'},
            {'name': 'कुतुब मीनार', 'type': 'ऐतिहासिक'}
        ],
        'markets': [
            {'name': 'चांदनी चौक', 'city': 'दिल्ली', 'specialty': 'पारंपरिक बाजार'},
            {'name': 'सरोजनी नगर', 'city': 'दिल्ली', 'specialty': 'कपड़े'}
        ]
    },
    # दक्षिण भारत
    'आंध्र प्रदेश': {
        'capital': 'अमरावती',
        'language': 'तेलुगू',
        'culture': {
            'dress': 'पुरुष: पंचे, महिला: साड़ी',
            'food': ['इडली', 'डोसा', 'पुलिहोरा', 'गोंगुरा पच्चड़ी'],
            'festivals': ['संक्रांति', 'उगादि', 'तीर्थ']
        },
        'famous_places': [
            {'name': 'तिरुपति बालाजी', 'type': 'धार्मिक'},
            {'name': 'अरकू वैली', 'type': 'हिल स्टेशन'},
            {'name': 'बेल्लम गुफाएं', 'type': 'प्राकृतिक'}
        ],
        'markets': [
            {'name': 'बीच रोड', 'city': 'विशाखापट्टनम', 'specialty': 'हस्तशिल्प'},
            {'name': 'नगरपालिका बाजार', 'city': 'विजयवाड़ा', 'specialty': 'फूल'}
        ]
    },
    'कर्नाटक': {
        'capital': 'बेंगलुरु',
        'language': 'कन्नड़',
        'culture': {
            'dress': 'पुरुष: पंचे, महिला: सीरे',
            'food': ['बिसिबेले भात', 'मैसूर पाक', 'दोसा', 'इडली'],
            'festivals': ['मैसूर दसरा', 'उगादि', 'कंबाला']
        },
        'famous_places': [
            {'name': 'मैसूर पैलेस', 'type': 'ऐतिहासिक'},
            {'name': 'हम्पी', 'type': 'पुरातात्विक'},
            {'name': 'कूर्ग', 'type': 'पहाड़ी स्टेशन'}
        ],
        'markets': [
            {'name': 'कमर्शियल स्ट्रीट', 'city': 'बेंगलुरु', 'specialty': 'शॉपिंग'},
            {'name': 'देवराज मार्केट', 'city': 'मैसूर', 'specialty': 'फूल'}
        ]
    },
    'केरल': {
        'capital': 'तिरुवनंतपुरम',
        'language': 'मलयालम',
        'culture': {
            'dress': 'पुरुष: मुंडु, महिला: साड़ी',
            'food': ['अप्पम', 'इडियप्पम', 'स्टू', 'साद्या'],
            'festivals': ['ओणम', 'विशु', 'तीयम']
        },
        'famous_places': [
            {'name': 'अलेप्पी हाउसबोट', 'type': 'बैकवाटर'},
            {'name': 'मुन्नार', 'type': 'हिल स्टेशन'},
            {'name': 'कोच्चि', 'type': 'ऐतिहासिक'}
        ],
        'markets': [
            {'name': 'ब्रॉडवे', 'city': 'कोच्चि', 'specialty': 'मसाले'},
            {'name': 'चालई बाजार', 'city': 'तिरुवनंतपुरम', 'specialty': 'आयुर्वेदिक'}
        ]
    },
    'तमिलनाडु': {
        'capital': 'चेन्नई',
        'language': 'तमिल',
        'culture': {
            'dress': 'पुरुष: वेष्टि, महिला: साड़ी',
            'food': ['इडली', 'डोसा', 'पोंगल', 'चिकन चेट्टीनाड'],
            'festivals': ['पोंगल', 'तमिल नववर्ष', 'थाईपुसम']
        },
        'famous_places': [
            {'name': 'मीनाक्षी मंदिर', 'type': 'धार्मिक'},
            {'name': 'मामल्लापुरम', 'type': 'ऐतिहासिक'},
            {'name': 'ऊटी', 'type': 'हिल स्टेशन'}
        ],
        'markets': [
            {'name': 'पार्क टाउन', 'city': 'चेन्नई', 'specialty': 'सोना'},
            {'name': 'ट्रिप्लिकेन बाजार', 'city': 'चेन्नई', 'specialty': 'कपड़े'}
        ]
    },
    'तेलंगाना': {
        'capital': 'हैदराबाद',
        'language': 'तेलुगू, उर्दू',
        'culture': {
            'dress': 'पुरुष: कुर्ता-पायजामा, महिला: साड़ी, सलवार',
            'food': ['हैदराबादी बिरयानी', 'हलीम', 'दोसा', 'पाया'],
            'festivals': ['बथुकम्मा', 'बोनालु', 'ईद']
        },
        'famous_places': [
            {'name': 'चारमीनार', 'type': 'ऐतिहासिक'},
            {'name': 'गोलकुंडा किला', 'type': 'ऐतिहासिक'},
            {'name': 'रामोजी फिल्म सिटी', 'type': 'मनोरंजन'}
        ],
        'markets': [
            {'name': 'लाड बाजार', 'city': 'हैदराबाद', 'specialty': 'चूड़ियाँ'},
            {'name': 'सुल्तान बाजार', 'city': 'हैदराबाद', 'specialty': 'मोती'}
        ]
    },
    # पूर्व भारत
    'पश्चिम बंगाल': {
        'capital': 'कोलकाता',
        'language': 'बंगाली',
        'culture': {
            'dress': 'पुरुष: धोती-पंजाबी, महिला: बंगाली साड़ी (लाल-सफेद)',
            'food': ['माछेर झोल', 'रसगुल्ला', 'संदेश', 'मिष्टी दोई'],
            'festivals': ['दुर्गा पूजा', 'काली पूजा', 'पौष संक्रांति', 'रथ यात्रा']
        },
        'famous_places': [
            {'name': 'विक्टोरिया मेमोरियल', 'type': 'ऐतिहासिक'},
            {'name': 'दार्जिलिंग', 'type': 'पहाड़ी स्टेशन'},
            {'name': 'सुंदरवन', 'type': 'राष्ट्रीय उद्यान'},
            {'name': 'बेलूर मठ', 'type': 'धार्मिक'}
        ],
        'markets': [
            {'name': 'न्यू मार्केट', 'city': 'कोलकाता', 'specialty': 'सब कुछ'},
            {'name': 'गड़िया हाट', 'city': 'कोलकाता', 'specialty': 'हस्तशिल्प'},
            {'name': 'कॉलेज स्ट्रीट', 'city': 'कोलकाता', 'specialty': 'किताबें'}
        ]
    },
    'बिहार': {
        'capital': 'पटना',
        'language': 'हिंदी, मैथिली, भोजपुरी',
        'culture': {
            'dress': 'पुरुष: धोती-कुर्ता, महिला: साड़ी',
            'food': ['लिट्टी-चोखा', 'सत्तू पराठा', 'खाजा', 'मखाना'],
            'festivals': ['छठ पूजा', 'सामा-चकेवा', 'जितिया', 'मधुश्रावणी']
        },
        'famous_places': [
            {'name': 'महाबोधि मंदिर', 'type': 'धार्मिक'},
            {'name': 'नालंदा विश्वविद्यालय', 'type': 'ऐतिहासिक'},
            {'name': 'विक्रमशिला', 'type': 'पुरातात्विक'},
            {'name': 'वाल्मीकि नगर', 'type': 'राष्ट्रीय उद्यान'}
        ],
        'markets': [
            {'name': 'हथुआ मार्केट', 'city': 'पटना', 'specialty': 'हस्तशिल्प'},
            {'name': 'मैसूर मार्केट', 'city': 'पटना', 'specialty': 'कपड़ा'}
        ]
    },
    'ओडिशा': {
        'capital': 'भुवनेश्वर',
        'language': 'ओड़िया',
        'culture': {
            'dress': 'पुरुष: धोती-कुर्ता, महिला: सम्बलपुरी साड़ी',
            'food': ['पखाल भात', 'छेना पोड़ा', 'दही बड़ा', 'रसगुल्ला'],
            'festivals': ['रथ यात्रा', 'दुर्गा पूजा', 'राजा पर्व', 'नुआखाई']
        },
        'famous_places': [
            {'name': 'कोणार्क सूर्य मंदिर', 'type': 'ऐतिहासिक'},
            {'name': 'जगन्नाथ पुरी', 'type': 'धार्मिक'},
            {'name': 'चिल्का झील', 'type': 'प्राकृतिक'},
            {'name': 'भितरकनिका', 'type': 'राष्ट्रीय उद्यान'}
        ],
        'markets': [
            {'name': 'बड़ाबाजार', 'city': 'कटक', 'specialty': 'चांदी के गहने'},
            {'name': 'एकाम्र हाट', 'city': 'भुवनेश्वर', 'specialty': 'हस्तशिल्प'}
        ]
    },
    'झारखंड': {
        'capital': 'रांची',
        'language': 'हिंदी, संथाली, हो',
        'culture': {
            'dress': 'पुरुष: धोती-गंजी, महिला: साड़ी',
            'food': ['ढुस्का', 'चिल्का रोटी', 'रुगड़ा', 'मड़ुआ की रोटी'],
            'festivals': ['सरहुल', 'करम', 'जावा', 'सोहराय']
        },
        'famous_places': [
            {'name': 'हुंडरू फॉल्स', 'type': 'प्राकृतिक'},
            {'name': 'बेतला नेशनल पार्क', 'type': 'वन्यजीव'},
            {'name': 'दशम फॉल्स', 'type': 'प्राकृतिक'},
            {'name': 'जगन्नाथपुर मंदिर', 'type': 'धार्मिक'}
        ],
        'markets': [
            {'name': 'रांची हाट', 'city': 'रांची', 'specialty': 'आदिवासी हस्तशिल्प'},
            {'name': 'मेन रोड', 'city': 'जमशेदपुर', 'specialty': 'शॉपिंग'}
        ]
    }
}

def get_state_details(state_name):
    """राज्य के विस्तृत आंकड़े"""
    return STATE_DETAILS.get(state_name)

@gov_bp.route('/')
def home():
    """मेरी सरकार का होम पेज"""
    # सभी यूनिक कैटेगरी और सब-कैटेगरी डैशबोर्ड के लिए लाएँ
    categories = db.session.query(GovernmentDepartment.category).distinct().all()
    states = db.session.query(GovernmentDepartment.state).distinct().all()
    return render_template('gov/home.html', categories=[c[0] for c in categories if c[0]], states=[s[0] for s in states if s[0]])
@gov_bp.route('/services')
def all_services():
    categories = GovernmentServices.get_categories()
    total = GovernmentServices.count_services()
    return render_template('gov/services.html', 
                         categories=categories,
                         total_services=total)

@gov_bp.route('/service/<string:service_name>')
def service_detail(service_name):
    service = GovernmentServices.get_service(service_name)
    if not service:
        return render_template('error.html', message="सेवा नहीं मिली"), 404
    return render_template('gov/service_detail.html', 
                         service_name=service_name, 
                         service=service)

@gov_bp.route('/services/category/<string:category>')
def services_by_category(category):
    categories = GovernmentServices.get_categories()
    services = categories.get(category, [])
    return render_template('gov/category_services.html',
                         category=category,
                         services=services)
@gov_bp.route('/companies')
def companies():
    """सभी कंपनियों का डैशबोर्ड"""
    return render_template('gov/companies.html')

@gov_bp.route('/search')
def search():
    """AI-लाइक सर्च एंडपॉइंट"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    # डेटाबेस में नाम, विवरण और टैग्स में सर्च करें
    results = GovernmentDepartment.query.filter(
        GovernmentDepartment.is_active == True
    ).filter(
        or_(
            GovernmentDepartment.name.ilike(f'%{query}%'),
            GovernmentDepartment.description.ilike(f'%{query}%'),
            GovernmentDepartment.search_tags.ilike(f'%{query}%'),
            GovernmentDepartment.category.ilike(f'%{query}%'),
            GovernmentDepartment.sub_category.ilike(f'%{query}%'),
            GovernmentDepartment.parent_ministry.ilike(f'%{query}%'),
            GovernmentDepartment.state.ilike(f'%{query}%'),
            GovernmentDepartment.city.ilike(f'%{query}%')
        )
    ).limit(20).all()

    # JSON रिस्पॉन्स बनाएँ
    result_list = [{
        'id': dept.id,
        'name': dept.name,
        'category': dept.category,
        'sub_category': dept.sub_category,
        'parent_ministry': dept.parent_ministry,
        'state': dept.state,
        'city': dept.city,
        'website_url': dept.website_url,
        'logo_url': dept.logo_url
    } for dept in results]
    
    return jsonify(result_list)

@gov_bp.route('/department/<int:dept_id>')
def department_detail(dept_id):
    """किसी एक विभाग का डिटेल पेज"""
    dept = GovernmentDepartment.query.get_or_404(dept_id)
    return render_template('gov/department.html', dept=dept)

@gov_bp.route('/category/<string:category_name>')
def category_view(category_name):
    """कैटेगरी के हिसाब से सभी विभाग दिखाएँ"""
    page = request.args.get('page', 1, type=int)
    departments = GovernmentDepartment.query.filter_by(category=category_name, is_active=True).paginate(page=page, per_page=20)
    return render_template('gov/category.html', departments=departments, category_name=category_name)
@gov_bp.route('/district/<string:state_name>/<string:district_name>')
def district_detail(state_name, district_name):
    """जिला डैशबोर्ड"""
    
    # District data (आप इसे database से ले सकते हैं)
    districts_data = {
        'महाराष्ट्र': {
            'नागपुर': {
                'headquarters': 'नागपुर',
                'population': '46,53,570',
                'area': '9,892',
                'literacy_rate': '89.5',
                'tehsils': '14',
                'dm_contact': '0712-2561234',
                'sp_contact': '0712-2565678',
                'hospital_contact': '0712-2741234',
                'helpline': '100',
                'gov_offices': [
                    {'name': 'नागपुर जिला कलेक्टर कार्यालय', 'url': 'https://nagpur.gov.in'},
                    {'name': 'नागपुर नगर निगम', 'url': 'https://nmcnagpur.gov.in'},
                    {'name': 'जिला पुलिस कार्यालय', 'url': 'https://nagpurpolice.gov.in'}
                ],
                'local_services': [
                    {'name': 'आधार केंद्र', 'url': 'https://uidai.gov.in'},
                    {'name': 'पासपोर्ट कार्यालय', 'url': 'https://passportindia.gov.in'},
                    {'name': 'जिला अस्पताल', 'url': 'https://nagpur.gov.in/hospital'}
                ]
            },
            'मुंबई': {
                'headquarters': 'मुंबई',
                'population': '1,24,42,373',
                'area': '603',
                'literacy_rate': '89.7',
                'tehsils': '24',
                'dm_contact': '022-22620211',
                'sp_contact': '022-22620222',
                'hospital_contact': '022-23084500',
                'helpline': '100',
                'gov_offices': [
                    {'name': 'मुंबई जिला कलेक्टर', 'url': 'https://mumbai.gov.in'},
                    {'name': 'बृहन्मुंबई नगर निगम', 'url': 'https://portal.mcgm.gov.in'}
                ],
                'local_services': [
                    {'name': 'आधार केंद्र', 'url': 'https://uidai.gov.in'},
                    {'name': 'पासपोर्ट कार्यालय', 'url': 'https://passportindia.gov.in'}
                ]
            },
            'पुणे': {
                'headquarters': 'पुणे',
                'population': '94,29,408',
                'area': '15,643',
                'literacy_rate': '86.2',
                'tehsils': '15',
                'dm_contact': '020-26123456',
                'sp_contact': '020-26123457',
                'hospital_contact': '020-26123458',
                'helpline': '100',
                'gov_offices': [
                    {'name': 'पुणे जिला कलेक्टर', 'url': 'https://pune.gov.in'},
                    {'name': 'पुणे नगर निगम', 'url': 'https://pmc.gov.in'}
                ],
                'local_services': [
                    {'name': 'आधार केंद्र', 'url': 'https://uidai.gov.in'},
                    {'name': 'पुणे जिला अस्पताल', 'url': 'https://pune.gov.in/hospital'}
                ]
            }
        },
        'गुजरात': {
            'अहमदाबाद': {
                'headquarters': 'अहमदाबाद',
                'population': '72,14,225',
                'area': '7,170',
                'literacy_rate': '85.3',
                'tehsils': '11',
                'dm_contact': '079-25520461',
                'sp_contact': '079-25520462',
                'hospital_contact': '079-22680000',
                'helpline': '100',
                'gov_offices': [
                    {'name': 'अहमदाबाद जिला कलेक्टर', 'url': 'https://ahmedabad.gujarat.gov.in'},
                    {'name': 'अहमदाबाद नगर निगम', 'url': 'https://ahmedabadcity.gov.in'}
                ],
                'local_services': [
                    {'name': 'आधार केंद्र', 'url': 'https://uidai.gov.in'},
                    {'name': 'पासपोर्ट कार्यालय', 'url': 'https://passportindia.gov.in'}
                ]
            }
        },
        'कर्नाटक': {
            'बेंगलुरु': {
                'headquarters': 'बेंगलुरु',
                'population': '1,21,27,356',
                'area': '2,196',
                'literacy_rate': '88.5',
                'tehsils': '28',
                'dm_contact': '080-22258888',
                'sp_contact': '080-22258889',
                'hospital_contact': '080-26789100',
                'helpline': '100',
                'gov_offices': [
                    {'name': 'बेंगलुरु जिला कलेक्टर', 'url': 'https://bengaluruurban.nic.in'},
                    {'name': 'बेंगलुरु नगर निगम', 'url': 'https://bbmp.gov.in'}
                ],
                'local_services': [
                    {'name': 'आधार केंद्र', 'url': 'https://uidai.gov.in'},
                    {'name': 'पासपोर्ट कार्यालय', 'url': 'https://passportindia.gov.in'}
                ]
            }
        }
    }
    
    # Get district data
    state_data = districts_data.get(state_name, {})
    district_info = state_data.get(district_name, {})
    
    if not district_info:
        return f"<h1>{district_name} जिले की जानकारी उपलब्ध नहीं है</h1>"
    
    return render_template('gov/districts/district_detail.html',
                         district_name=district_name,
                         state_name=state_name,
                         district_headquarters=district_info.get('headquarters', ''),
                         population=district_info.get('population', ''),
                         area=district_info.get('area', ''),
                         literacy_rate=district_info.get('literacy_rate', ''),
                         tehsils=district_info.get('tehsils', ''),
                         dm_contact=district_info.get('dm_contact', ''),
                         sp_contact=district_info.get('sp_contact', ''),
                         hospital_contact=district_info.get('hospital_contact', ''),
                         helpline=district_info.get('helpline', ''),
                         gov_offices=district_info.get('gov_offices', []),
                         local_services=district_info.get('local_services', []))
@gov_bp.route('/direct-services')
def direct_services():
    """सभी सरकारी सेवाएं - Direct Links"""
    return render_template('gov/direct_services.html')

@gov_bp.route('/state/<string:state_name>')
def state_view(state_name):
    """राज्य का पूरा डैशबोर्ड"""
    page = request.args.get('page', 1, type=int)
    departments = GovernmentDepartment.query.filter_by(state=state_name, is_active=True).paginate(page=page, per_page=20)
    
    # राज्य के आंकड़े
    state_stats = {
        'name': state_name,
        'total_depts': departments.total,
        'categories': db.session.query(GovernmentDepartment.category).filter_by(state=state_name).distinct().count()
    }
    
    # राज्य-विशेष डेटा
    state_details = get_state_details(state_name)
    
    # Debug print
    print(f"State: {state_name}, Details found: {bool(state_details)}")
    
    return render_template('gov/state_dashboard.html', 
                         departments=departments,
                         state=state_stats,
                         details=state_details)