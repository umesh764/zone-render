# gov_services.py

class GovernmentServices:
    """सभी सरकारी सेवाओं की लिस्ट"""
    
    SERVICES = {
        # **** वित्त एवं कर (Finance & Tax) ****
        'पैन कार्ड': {
            'category': 'वित्त एवं कर',
            'url': 'https://www.incometax.gov.in/',
            'description': 'पैन कार्ड के लिए आवेदन करें, अपडेट करें या डाउनलोड करें',
            'type': 'document',
            'ministry': 'Income Tax Department'
        },
        'आयकर रिटर्न (ITR)': {
            'category': 'वित्त एवं कर',
            'url': 'https://www.incometax.gov.in/itr',
            'description': 'आयकर रिटर्न भरें, स्टेटस चेक करें',
            'type': 'service',
            'ministry': 'Income Tax Department'
        },
        'जीएसटी (GST)': {
            'category': 'वित्त एवं कर',
            'url': 'https://www.gst.gov.in',
            'description': 'जीएसटी रजिस्ट्रेशन, रिटर्न फाइलिंग, पेमेंट',
            'type': 'service',
            'ministry': 'Central Board of Indirect Taxes'
        },
        'ई-वे बिल (e-Way Bill)': {
            'category': 'वित्त एवं कर',
            'url': 'https://ewaybill.nic.in',
            'description': 'माल परिवहन के लिए ई-वे बिल जनरेट करें',
            'type': 'service',
            'ministry': 'GST Network'
        },
        'ई-इनवॉइस (e-Invoice)': {
            'category': 'वित्त एवं कर',
            'url': 'https://einvoice1.gst.gov.in',
            'description': 'जीएसटी के लिए इलेक्ट्रॉनिक इनवॉइस सिस्टम',
            'type': 'service',
            'ministry': 'GST Network'
        },

        # **** पहचान एवं दस्तावेज़ (Identity) ****
        'आधार कार्ड': {
            'category': 'पहचान एवं दस्तावेज़',
            'url': 'https://uidai.gov.in',
            'description': 'आधार कार्ड डाउनलोड करें, अपडेट करें, वेरिफाई करें',
            'type': 'document',
            'ministry': 'UIDAI' 
        },
        'डिजिलॉकर (DigiLocker)': {
            'category': 'पहचान एवं दस्तावेज़',
            'url': 'https://www.digilocker.gov.in',
            'description': 'डिजिटल दस्तावेज़ स्टोर करें और शेयर करें (6 करोड़+ यूजर्स)',
            'type': 'service',
            'ministry': 'MeitY'
        },
        'मेरी पहचान (MeriPehchaan)': {
            'category': 'पहचान एवं दस्तावेज़',
            'url': 'https://meripehchaan.gov.in',
            'description': 'सिंगल साइन-ऑन सेवा, एक लॉगिन से सभी सरकारी पोर्टल',
            'type': 'service',
            'ministry': 'GST Network'
        },

        # **** चुनाव एवं लोकतंत्र (Elections) ****
        'वोटर आईडी (EPIC)': {
            'category': 'चुनाव एवं लोकतंत्र',
            'url': 'https://nvsp.in',
            'description': 'वोटर कार्ड बनवाएं, नाम चेक करें, अपडेट करें',
            'type': 'document',
            'ministry': 'Election Commission'
        },
        'वोटर हेल्पलाइन ऐप': {
            'category': 'चुनाव एवं लोकतंत्र',
            'url': 'https://voterportal.eci.gov.in',
            'description': 'वोटर से जुड़ी सभी सेवाएं मोबाइल पर',
            'type': 'service',
            'ministry': 'Election Commission'
        },
        'माईगव (MyGov)': {
            'category': 'चुनाव एवं लोकतंत्र',
            'url': 'https://www.mygov.in',
            'description': 'सरकारी योजनाओं में सुझाव दें, पोल में भाग लें',
            'type': 'service',
            'ministry': 'MeitY'
        },

        # **** शिक्षा (Education) ****
        'दीक्षा (DIKSHA)': {
            'category': 'शिक्षा',
            'url': 'https://diksha.gov.in',
            'description': 'एक राष्ट्र, एक डिजिटल प्लेटफॉर्म - स्कूली शिक्षा के लिए',
            'type': 'service',
            'ministry': 'NCERT, Ministry of Education'
        },
        'ई-ग्रंथालय (eGranthalaya)': {
            'category': 'शिक्षा',
            'url': 'https://egranthalaya.nic.in',
            'description': 'डिजिटल लाइब्रेरी मैनेजमेंट सिस्टम',
            'type': 'service',
            'ministry': 'NIC'
        },
        'एनपीटीईएल (NPTEL)': {
            'category': 'शिक्षा',
            'url': 'https://nptel.ac.in',
            'description': 'ऑनलाइन कोर्स और सर्टिफिकेशन',
            'type': 'service',
            'ministry': 'IITs, Ministry of Education'
        },
        'स्कॉलरशिप (NSP)': {
            'category': 'शिक्षा',
            'url': 'https://scholarships.gov.in',
            'description': 'राष्ट्रीय छात्रवृत्ति पोर्टल',
            'type': 'scheme',
            'ministry': 'Ministry of Education'
        },
        'ई-पाठशाला (ePathshala)': {
            'category': 'शिक्षा',
            'url': 'https://epathshala.nic.in',
            'description': 'डिजिटल शिक्षा संसाधन, एनसीईआरटी की किताबें',
            'type': 'service',
            'ministry': 'NCERT'
        },

        # **** रोजगार एवं करियर (Employment) ****
        'नेशनल करियर सर्विस (NCS)': {
            'category': 'रोजगार एवं करियर',
            'url': 'https://www.ncs.gov.in',
            'description': 'सरकारी और प्राइवेट नौकरियां, करियर काउंसलिंग (6.43 करोड़+ वैकेंसी)',
            'type': 'service',
            'ministry': 'Ministry of Labour & Employment'
        },
        'ई-श्रम (eShram)': {
            'category': 'रोजगार एवं करियर',
            'url': 'https://eshram.gov.in',
            'description': 'असंगठित क्षेत्र के श्रमिकों का राष्ट्रीय डेटाबेस',
            'type': 'service',
            'ministry': 'Ministry of Labour'
        },
        'पीएम कौशल विकास योजना (PMKVY)': {
            'category': 'रोजगार एवं करियर',
            'url': 'https://www.pmkvyofficial.org',
            'description': 'स्किल डेवलपमेंट और ट्रेनिंग',
            'type': 'scheme',
            'ministry': 'MSDE'
        },
        'आजीविका (NRLM)': {
            'category': 'रोजगार एवं करियर',
            'url': 'https://aajeevika.gov.in',
            'description': 'ग्रामीण गरीबी उन्मूलन और आजीविका मिशन',
            'type': 'scheme',
            'ministry': 'Ministry of Rural Development'
        },
        'दीनदयाल उपाध्याय ग्रामीण कौशल योजना': {
            'category': 'रोजगार एवं करियर',
            'url': 'http://ddugky.info',
            'description': 'ग्रामीण युवाओं के लिए कौशल विकास',
            'type': 'scheme',
            'ministry': 'Ministry of Rural Development'
        },

        # **** स्वास्थ्य (Health) ****
        'आयुष्मान भारत (PMJAY)': {
            'category': 'स्वास्थ्य',
            'url': 'https://pmjay.gov.in',
            'description': 'आयुष्मान कार्ड बनवाएं, 5 लाख तक का स्वास्थ्य बीमा',
            'type': 'scheme',
            'ministry': 'Ministry of Health'
        },
        'ऑनलाइन रजिस्ट्रेशन सिस्टम (ORS)': {
            'category': 'स्वास्थ्य',
            'url': 'https://ors.gov.in',
            'description': 'सरकारी अस्पतालों में ऑनलाइन अपॉइंटमेंट बुक करें',
            'type': 'service',
            'ministry': 'Ministry of Health'
        },
        'कोविन (CoWIN)': {
            'category': 'स्वास्थ्य',
            'url': 'https://www.cowin.gov.in',
            'description': 'वैक्सीनेशन सर्टिफिकेट डाउनलोड करें',
            'type': 'service',
            'ministry': 'Ministry of Health'
        },

        # **** परिवहन (Transport) ****
        'परिवहन (Parivahan)': {
            'category': 'परिवहन',
            'url': 'https://parivahan.gov.in',
            'description': 'ड्राइविंग लाइसेंस, वाहन रजिस्ट्रेशन, ई-चालान',
            'type': 'service',
            'ministry': 'Ministry of Road Transport'
        },
        'सारथी (Sarathi)': {
            'category': 'परिवहन',
            'url': 'https://sarathi.parivahan.gov.in',
            'description': 'ड्राइविंग लाइसेंस बनवाएं, रिन्यू करें',
            'type': 'service',
            'ministry': 'Ministry of Road Transport'
        },
        'वाहन (Vahan)': {
            'category': 'परिवहन',
            'url': 'https://vahan.parivahan.gov.in',
            'description': 'वाहन रजिस्ट्रेशन, टैक्स भुगतान, आरसी डाउनलोड',
            'type': 'service',
            'ministry': 'Ministry of Road Transport' 
        },

        # **** कृषि (Agriculture) ****
        'साथी (SATHI)': {
            'category': 'कृषि',
            'url': 'https://sathi.gov.in',
            'description': 'बीज ट्रेसेबिलिटी और प्रमाणीकरण प्रणाली',
            'type': 'service',
            'ministry': 'Ministry of Agriculture' 
        },
        'फ्रूट्स (FRUITS)': {
            'category': 'कृषि',
            'url': 'https://fruits.gov.in',
            'description': 'किसान रजिस्ट्रेशन और यूनिफाइड बेनिफिशियरी सिस्टम',
            'type': 'service',
            'ministry': 'Ministry of Agriculture'
        },
        'ई-एनएएम (eNAM)': {
            'category': 'कृषि',
            'url': 'https://enam.gov.in',
            'description': 'राष्ट्रीय कृषि बाजार - ऑनलाइन मंडी',
            'type': 'service',
            'ministry': 'Ministry of Agriculture'
        },

        # **** कल्याण एवं योजनाएं (Welfare) ****
        'माईस्कीम (myScheme)': {
            'category': 'कल्याण एवं योजनाएं',
            'url': 'https://www.myscheme.gov.in',
            'description': '4000+ सरकारी योजनाएं एक ही जगह, पात्रता चेक करें',
            'type': 'service',
            'ministry': 'MeitY'
        },
        'उमंग (UMANG)': {
            'category': 'कल्याण एवं योजनाएं',
            'url': 'https://umang.gov.in',
            'description': '210+ विभागों की 2000+ सेवाएं एक ऐप पर (9.63 करोड़ यूजर्स)',
            'type': 'service',
            'ministry': 'MeitY'
        },
        'जीवन प्रमाण (Jeevan Pramaan)': {
            'category': 'कल्याण एवं योजनाएं',
            'url': 'https://jeevanpramaan.gov.in',
            'description': 'पेंशनभोगियों के लिए डिजिटल लाइफ सर्टिफिकेट',
            'type': 'service',
            'ministry': 'Ministry of Personnel'
        },

        'पीएम स्वनिधि (PM SVANidhi)': {
            'category': 'कल्याण एवं योजनाएं',
            'url': 'https://pmsvanidhi.mohua.gov.in',
            'description': 'स्ट्रीट वेंडर्स के लिए कार्यशील पूंजी ऋण',
            'type': 'scheme',
            'ministry': 'Ministry of Housing & Urban Affairs'
        },

        # **** यात्रा एवं पर्यटन (Travel) ****
        'पासपोर्ट': {
            'category': 'यात्रा एवं पर्यटन',
            'url': 'https://passportindia.gov.in',
            'description': 'पासपोर्ट के लिए अप्लाई करें, अपॉइंटमेंट बुक करें',
            'type': 'document',
            'ministry': 'Ministry of External Affairs'
        },
        'भारत ऑनलाइन वीज़ा': {
            'category': 'यात्रा एवं पर्यटन',
            'url': 'https://indianvisaonline.gov.in',
            'description': 'भारत आने के लिए ई-वीज़ा आवेदन',
            'type': 'service',
            'ministry': 'Ministry of Home Affairs'
        },

        # **** न्याय एवं कानून (Justice) ****
        'ई-कोर्ट्स (eCourts)': {
            'category': 'न्याय एवं कानून',
            'url': 'https://ecourts.gov.in',
            'description': 'केस स्टेटस देखें, ऑर्डर डाउनलोड करें',
            'type': 'service',
            'ministry': 'Supreme Court'
        },
        'ई-फाइलिंग (eFiling)': {
            'category': 'न्याय एवं कानून',
            'url': 'https://efiling.ecourts.gov.in',
            'description': 'कोर्ट में इलेक्ट्रॉनिक केस फाइलिंग',
            'type': 'service',
            'ministry': 'Supreme Court'
        }
    }
     @staticmethod
    def get_department_by_type(dept_type):
        """Get department by type"""
        # Temporary implementation
        return None 
   
    @classmethod
    def get_all_services(cls):
        return cls.SERVICES
    
    @classmethod
    def get_service(cls, name):
        return cls.SERVICES.get(name)
    
    @classmethod
    def get_categories(cls):
        categories = {}
        for service_name, service_data in cls.SERVICES.items():
            cat = service_data['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'name': service_name,
                'data': service_data
            })
        return categories
    
    @classmethod
    def count_services(cls):
        return len(cls.SERVICES)
    """Government Services Helper Module"""

class GovernmentServices:
    """Helper class for government services"""
    
    @staticmethod
    def get_categories():
        """Get all service categories"""
        return ['Passport', 'Driving License', 'PAN Card', 'Aadhaar', 'Voter ID', 'Birth Certificate', 'Marriage Certificate']
    
    @staticmethod
    def count_services():
        """Count total services"""
        return len(GovernmentServices.get_categories())
    
    @staticmethod
    def get_service(service_name):
        """Get service details by name"""
        services = {
            'Passport': {
                'name': 'Passport',
                'description': 'नया पासपोर्ट बनवाने, रिन्यूअल और संशोधन के लिए आवेदन करें',
                'fees': 1500,
                'processing_time': '7-15 दिन',
                'documents': ['आधार कार्ड', 'जन्म प्रमाण पत्र', 'पता प्रमाण', 'शैक्षणिक प्रमाण पत्र']
            },
            'Driving License': {
                'name': 'Driving License',
                'description': 'लर्नर लाइसेंस, पक्का लाइसेंस और रिन्यूअल के लिए आवेदन करें',
                'fees': 500,
                'processing_time': '15-30 दिन',
                'documents': ['आधार कार्ड', 'पता प्रमाण', 'आयु प्रमाण', 'ड्राइविंग टेस्ट']
            },
            'PAN Card': {
                'name': 'PAN Card',
                'description': 'नया पैन कार्ड, सुधार और रिप्रिंट के लिए आवेदन करें',
                'fees': 107,
                'processing_time': '15-30 दिन',
                'documents': ['आधार कार्ड', 'पता प्रमाण', 'पहचान प्रमाण']
            },
            'Aadhaar': {
                'name': 'Aadhaar',
                'description': 'नया आधार कार्ड, अपडेट और सुधार के लिए आवेदन करें',
                'fees': 0,
                'processing_time': '30-45 दिन',
                'documents': ['जन्म प्रमाण पत्र', 'पता प्रमाण', 'पहचान प्रमाण']
            }
        }
        return services.get(service_name, None)
