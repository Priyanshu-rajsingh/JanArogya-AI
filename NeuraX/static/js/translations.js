// ====== NeuraX Multi-Language Translation System ======

const TRANSLATIONS = {
  en: {
    // Navbar
    nav_home: "Home", nav_patient: "Patient Portal", nav_hospital: "Hospital Portal",
    nav_encrypted: "AES-256 Encrypted", lang_label: "Language",
    // Patient Info
    patient_title: "AI Health Screening", patient_subtitle: "Enter your details for AI-powered health risk analysis and disease prediction",
    section_info: "Patient Information", lbl_name: "Full Name", lbl_age: "Age",
    lbl_gender: "Gender", lbl_location: "Location", lbl_contact: "Contact Number",
    ph_name: "Enter your full name", ph_age: "Enter age", ph_location: "City or village",
    ph_contact: "Phone number", opt_gender: "Select Gender", opt_male: "Male",
    opt_female: "Female", opt_other: "Other",
    // Symptoms
    section_symptoms: "Select Your Symptoms", symptoms_desc: "Click on all symptoms that you are currently experiencing",
    selected_count: "Selected:", symptom_unit: "symptom(s)",
    section_describe: "Describe Your Symptoms",
    describe_text: "Write about your symptoms in detail — when they started, their severity, or any other information you think is relevant.",
    ph_describe: "E.g., I've been having a severe headache for the past 3 days, mostly on the right side. The pain gets worse at night and I also feel nauseous after eating...",
    // Upload
    section_upload: "Upload Medical Images (Optional)",
    upload_desc: "Upload photos of skin conditions, injuries, test reports, or any relevant medical documents for the doctor to review.",
    upload_drag: "Drag & drop images here", upload_or: "or click to browse files",
    upload_formats: "Supports: JPG, PNG, WEBP, PDF — Max 5MB per file",
    // Vitals
    section_vitals: "Vital Parameters",
    vitals_desc: "Enter your current vital signs if available. Only the vitals you enter will appear in the analysis.",
    lbl_hr: "Heart Rate (BPM)", lbl_sbp: "Systolic Blood Pressure",
    lbl_dbp: "Diastolic Blood Pressure", lbl_temp: "Body Temperature (°F)",
    lbl_spo2: "SpO2 Level (%)", lbl_bmi: "BMI",
    // Button
    btn_analyze: "Analyze Health Risk", btn_note: "Your data is processed by our AI model and encrypted end-to-end",
    // Results
    risk_score_label: "RISK SCORE", encrypted_result: "Encrypted Result",
    section_disease: "Possible Disease Predictions",
    disease_desc: "Based on your symptoms, the AI model has identified the following possible conditions:",
    section_risk: "Risk Level Analysis", section_triage: "Triage Classification",
    section_factors: "Contributing Factors (XAI)", section_vitals_result: "Vital Signs Analysis",
    section_hospitals: "Recommended Hospitals Near You",
    hospitals_desc: "Based on the specialist needed for your condition, here are nearby hospitals:",
    detecting_location: "Detecting your location...",
    lbl_patient_id: "Your Patient ID",
    patient_id_note: "Save this ID for reference. Your records have been securely sent to the hospital dashboard.",
    btn_new: "New Screening", btn_print: "Print Report",
    btn_directions: "Get Directions", btn_notify: "Notify Hospital",
    // Footer
    footer_text: "© 2026 NeuraX — AI-Powered Remote Healthcare Platform",
    footer_hipaa: "HIPAA Compliant",
    // Toasts
    toast_analysis_done: "Health analysis complete!",
    toast_notify_sent: "Alert sent! They will be expecting you.",
    // Misc
    matching_symptoms: "Matching symptoms:",
    no_factors: "No significant contributing factors identified.",
    no_disease: "Could not determine specific conditions from the provided symptoms. Please consult a doctor.",
    loc_detected: "Location detected — showing nearest hospitals",
    loc_unavail: "Location unavailable — showing top-rated hospitals"
  },
  hi: {
    nav_home: "होम", nav_patient: "रोगी पोर्टल", nav_hospital: "अस्पताल पोर्टल",
    nav_encrypted: "AES-256 एन्क्रिप्टेड", lang_label: "भाषा",
    patient_title: "AI स्वास्थ्य जांच", patient_subtitle: "AI-संचालित स्वास्थ्य जोखिम विश्लेषण और रोग पूर्वानुमान के लिए अपने विवरण दर्ज करें",
    section_info: "रोगी की जानकारी", lbl_name: "पूरा नाम", lbl_age: "आयु",
    lbl_gender: "लिंग", lbl_location: "स्थान", lbl_contact: "संपर्क नंबर",
    ph_name: "अपना पूरा नाम दर्ज करें", ph_age: "आयु दर्ज करें", ph_location: "शहर या गाँव",
    ph_contact: "फ़ोन नंबर", opt_gender: "लिंग चुनें", opt_male: "पुरुष",
    opt_female: "महिला", opt_other: "अन्य",
    section_symptoms: "अपने लक्षण चुनें", symptoms_desc: "उन सभी लक्षणों पर क्लिक करें जो आप अनुभव कर रहे हैं",
    selected_count: "चयनित:", symptom_unit: "लक्षण",
    section_describe: "अपने लक्षणों का वर्णन करें",
    describe_text: "अपने लक्षणों के बारे में विस्तार से लिखें — वे कब शुरू हुए, उनकी गंभीरता, या कोई अन्य जानकारी।",
    ph_describe: "उदा., मुझे पिछले 3 दिनों से तेज सिरदर्द हो रहा है, ज्यादातर दाहिनी तरफ...",
    section_upload: "मेडिकल छवियां अपलोड करें (वैकल्पिक)",
    upload_desc: "त्वचा की स्थिति, चोटों, परीक्षण रिपोर्ट, या किसी प्रासंगिक चिकित्सा दस्तावेज़ की फ़ोटो अपलोड करें।",
    upload_drag: "छवियां यहां खींचें और छोड़ें", upload_or: "या फ़ाइलें ब्राउज़ करें",
    upload_formats: "समर्थित: JPG, PNG, WEBP, PDF — अधिकतम 5MB प्रति फ़ाइल",
    section_vitals: "महत्वपूर्ण पैरामीटर",
    vitals_desc: "यदि उपलब्ध हो तो अपने वर्तमान महत्वपूर्ण संकेत दर्ज करें। केवल आपके द्वारा दर्ज किए गए संकेत विश्लेषण में दिखाई देंगे।",
    lbl_hr: "हृदय गति (BPM)", lbl_sbp: "सिस्टोलिक रक्तचाप",
    lbl_dbp: "डायस्टोलिक रक्तचाप", lbl_temp: "शरीर का तापमान (°F)",
    lbl_spo2: "SpO2 स्तर (%)", lbl_bmi: "BMI",
    btn_analyze: "स्वास्थ्य जोखिम का विश्लेषण करें", btn_note: "आपका डेटा AI मॉडल द्वारा संसाधित और एंड-टू-एंड एन्क्रिप्टेड है",
    risk_score_label: "जोखिम स्कोर", encrypted_result: "एन्क्रिप्टेड परिणाम",
    section_disease: "संभावित रोग पूर्वानुमान",
    disease_desc: "आपके लक्षणों के आधार पर, AI मॉडल ने निम्नलिखित संभावित स्थितियों की पहचान की है:",
    section_risk: "जोखिम स्तर विश्लेषण", section_triage: "ट्राइएज वर्गीकरण",
    section_factors: "योगदान कारक (XAI)", section_vitals_result: "महत्वपूर्ण संकेत विश्लेषण",
    section_hospitals: "आपके पास अनुशंसित अस्पताल",
    hospitals_desc: "आपकी स्थिति के लिए आवश्यक विशेषज्ञ के आधार पर, यहां नज़दीकी अस्पताल हैं:",
    detecting_location: "आपका स्थान खोजा जा रहा है...",
    lbl_patient_id: "आपकी रोगी ID",
    patient_id_note: "संदर्भ के लिए इस ID को सहेजें। आपके रिकॉर्ड सुरक्षित रूप से अस्पताल डैशबोर्ड पर भेजे गए हैं।",
    btn_new: "नई जांच", btn_print: "रिपोर्ट प्रिंट करें",
    btn_directions: "दिशा-निर्देश", btn_notify: "अस्पताल को सूचित करें",
    footer_text: "© 2026 NeuraX — AI-संचालित दूरस्थ स्वास्थ्य सेवा मंच",
    footer_hipaa: "HIPAA अनुपालन",
    toast_analysis_done: "स्वास्थ्य विश्लेषण पूर्ण!",
    toast_notify_sent: "सूचना भेजी गई! वे आपकी प्रतीक्षा करेंगे।",
    matching_symptoms: "मेल खाते लक्षण:",
    no_factors: "कोई महत्वपूर्ण योगदान कारक नहीं पाए गए।",
    no_disease: "दिए गए लक्षणों से विशिष्ट स्थितियां निर्धारित नहीं हो सकीं। कृपया डॉक्टर से परामर्श करें।",
    loc_detected: "स्थान पता लगा — निकटतम अस्पताल दिखा रहे हैं",
    loc_unavail: "स्थान अनुपलब्ध — शीर्ष रेटेड अस्पताल दिखा रहे हैं"
  },
  te: {
    nav_home: "హోమ్", nav_patient: "రోగి పోర్టల్", nav_hospital: "ఆసుపత్రి పోర్టల్",
    nav_encrypted: "AES-256 ఎన్‌క్రిప్టెడ్", lang_label: "భాష",
    patient_title: "AI ఆరోగ్య స్క్రీనింగ్", patient_subtitle: "AI-ఆధారిత ఆరోగ్య ప్రమాద విశ్లేషణ కోసం మీ వివరాలను నమోదు చేయండి",
    section_info: "రోగి సమాచారం", lbl_name: "పూర్తి పేరు", lbl_age: "వయస్సు",
    lbl_gender: "లింగం", lbl_location: "ప్రాంతం", lbl_contact: "సంప్రదింపు నంబర్",
    ph_name: "మీ పూర్తి పేరు నమోదు చేయండి", ph_age: "వయస్సు నమోదు చేయండి",
    ph_location: "నగరం లేదా గ్రామం", ph_contact: "ఫోన్ నంబర్",
    opt_gender: "లింగాన్ని ఎంచుకోండి", opt_male: "పురుషుడు", opt_female: "స్త్రీ", opt_other: "ఇతర",
    section_symptoms: "మీ లక్షణాలను ఎంచుకోండి", symptoms_desc: "మీరు అనుభవిస్తున్న అన్ని లక్షణాలపై క్లిక్ చేయండి",
    selected_count: "ఎంచుకున్నవి:", symptom_unit: "లక్షణం(లు)",
    section_describe: "మీ లక్షణాలను వివరించండి",
    describe_text: "మీ లక్షణాల గురించి వివరంగా రాయండి — అవి ఎప్పుడు ప్రారంభమయ్యాయి, తీవ్రత మొదలైనవి.",
    ph_describe: "ఉదా., నాకు గత 3 రోజులుగా తీవ్రమైన తలనొప్పి ఉంది...",
    section_upload: "వైద్య చిత్రాలను అప్‌లోడ్ చేయండి (ఐచ్ఛికం)",
    upload_desc: "చర్మ పరిస్థితులు, గాయాలు, పరీక్ష నివేదికల ఫోటోలను అప్‌లోడ్ చేయండి.",
    upload_drag: "చిత్రాలను ఇక్కడ లాగి వదలండి", upload_or: "లేదా ఫైళ్లను బ్రౌజ్ చేయండి",
    upload_formats: "మద్దతు: JPG, PNG, WEBP, PDF — ఫైల్‌కు గరిష్టంగా 5MB",
    section_vitals: "ప్రముఖ పారామీటర్లు",
    vitals_desc: "అందుబాటులో ఉంటే మీ ప్రస్తుత ప్రముఖ సంకేతాలను నమోదు చేయండి.",
    lbl_hr: "హృదయ స్పందన (BPM)", lbl_sbp: "సిస్టోలిక్ రక్తపోటు",
    lbl_dbp: "డయాస్టోలిక్ రక్తపోటు", lbl_temp: "శరీర ఉష్ణోగ్రత (°F)",
    lbl_spo2: "SpO2 స్థాయి (%)", lbl_bmi: "BMI",
    btn_analyze: "ఆరోగ్య ప్రమాదాన్ని విశ్లేషించండి", btn_note: "మీ డేటా AI మోడల్ ద్వారా ప్రాసెస్ చేయబడింది",
    risk_score_label: "ప్రమాద స్కోర్", encrypted_result: "ఎన్‌క్రిప్టెడ్ ఫలితం",
    section_disease: "సాధ్యమైన వ్యాధి అంచనాలు",
    disease_desc: "మీ లక్షణాల ఆధారంగా, AI మోడల్ క్రింది సాధ్యమైన పరిస్థితులను గుర్తించింది:",
    section_risk: "ప్రమాద స్థాయి విశ్లేషణ", section_triage: "ట్రయేజ్ వర్గీకరణ",
    section_factors: "దోహద కారకాలు (XAI)", section_vitals_result: "ప్రముఖ సంకేతాల విశ్లేషణ",
    section_hospitals: "మీ సమీపంలోని సిఫార్సు చేసిన ఆసుపత్రులు",
    hospitals_desc: "మీ పరిస్థితికి అవసరమైన నిపుణుల ఆధారంగా, ఇక్కడ సమీప ఆసుపత్రులు ఉన్నాయి:",
    detecting_location: "మీ స్థానాన్ని గుర్తిస్తోంది...",
    lbl_patient_id: "మీ రోగి ID", patient_id_note: "సూచన కోసం ఈ IDని భద్రపరచండి.",
    btn_new: "కొత్త స్క్రీనింగ్", btn_print: "నివేదిక ప్రింట్",
    btn_directions: "దిశలు పొందండి", btn_notify: "ఆసుపత్రికి తెలియజేయండి",
    footer_text: "© 2026 NeuraX — AI-ఆధారిత రిమోట్ హెల్త్‌కేర్ ప్లాట్‌ఫారమ్", footer_hipaa: "HIPAA అనుసరణ",
    toast_analysis_done: "ఆరోగ్య విశ్లేషణ పూర్తయింది!", toast_notify_sent: "హెచ్చరిక పంపబడింది!",
    matching_symptoms: "సరిపోలే లక్షణాలు:", no_factors: "ముఖ్యమైన దోహద కారకాలు గుర్తించబడలేదు.",
    no_disease: "అందించిన లక్షణాల నుండి నిర్దిష్ట పరిస్థితులను నిర్ణయించలేకపోయాము.", loc_detected: "స్థానం గుర్తించబడింది",
    loc_unavail: "స్థానం అందుబాటులో లేదు"
  },
  ta: {
    nav_home: "முகப்பு", nav_patient: "நோயாளி போர்டல்", nav_hospital: "மருத்துவமனை போர்டல்",
    nav_encrypted: "AES-256 மறையாக்கம்", lang_label: "மொழி",
    patient_title: "AI சுகாதார பரிசோதனை", patient_subtitle: "AI அடிப்படையிலான சுகாதார ஆபத்து பகுப்பாய்வுக்கு உங்கள் விவரங்களை உள்ளிடவும்",
    section_info: "நோயாளி தகவல்", lbl_name: "முழு பெயர்", lbl_age: "வயது",
    lbl_gender: "பாலினம்", lbl_location: "இடம்", lbl_contact: "தொடர்பு எண்",
    ph_name: "முழு பெயரை உள்ளிடவும்", ph_age: "வயதை உள்ளிடவும்",
    ph_location: "நகரம் அல்லது கிராமம்", ph_contact: "தொலைபேசி எண்",
    opt_gender: "பாலினத்தைத் தேர்ந்தெடுக்கவும்", opt_male: "ஆண்", opt_female: "பெண்", opt_other: "மற்ற",
    section_symptoms: "உங்கள் அறிகுறிகளைத் தேர்ந்தெடுக்கவும்", symptoms_desc: "நீங்கள் அனுபவிக்கும் அனைத்து அறிகுறிகளையும் கிளிக் செய்யவும்",
    selected_count: "தேர்ந்தெடுக்கப்பட்டவை:", symptom_unit: "அறிகுறி(கள்)",
    section_describe: "உங்கள் அறிகுறிகளை விவரிக்கவும்",
    describe_text: "உங்கள் அறிகுறிகளைப் பற்றி விரிவாக எழுதவும்.",
    ph_describe: "எ.கா., கடந்த 3 நாட்களாக கடுமையான தலைவலி...",
    section_upload: "மருத்துவ படங்களை பதிவேற்றவும் (விருப்பம்)",
    upload_desc: "தோல் நிலைகள், காயங்கள், பரிசோதனை அறிக்கைகளின் புகைப்படங்களை பதிவேற்றவும்.",
    upload_drag: "படங்களை இங்கே இழுக்கவும்", upload_or: "அல்லது கோப்புகளை உலாவவும்",
    upload_formats: "ஆதரவு: JPG, PNG, WEBP, PDF — கோப்புக்கு அதிகபட்சம் 5MB",
    section_vitals: "முக்கிய அளவுருக்கள்",
    vitals_desc: "கிடைத்தால் உங்கள் தற்போதைய உயிர்நாடி அறிகுறிகளை உள்ளிடவும்.",
    lbl_hr: "இதய துடிப்பு (BPM)", lbl_sbp: "சிஸ்டாலிக் இரத்த அழுத்தம்",
    lbl_dbp: "டயஸ்டாலிக் இரத்த அழுத்தம்", lbl_temp: "உடல் வெப்பநிலை (°F)",
    lbl_spo2: "SpO2 நிலை (%)", lbl_bmi: "BMI",
    btn_analyze: "சுகாதார ஆபத்தை பகுப்பாய்வு செய்யவும்", btn_note: "உங்கள் தரவு AI மாதிரியால் செயலாக்கப்படுகிறது",
    risk_score_label: "ஆபத்து மதிப்பெண்", encrypted_result: "மறையாக்கப்பட்ட முடிவு",
    section_disease: "சாத்தியமான நோய் கணிப்புகள்",
    disease_desc: "உங்கள் அறிகுறிகளின் அடிப்படையில், AI சாத்தியமான நிலைகளை கண்டறிந்துள்ளது:",
    section_risk: "ஆபத்து நிலை பகுப்பாய்வு", section_triage: "ட்ரையேஜ் வகைப்பாடு",
    section_factors: "பங்களிப்பு காரணிகள் (XAI)", section_vitals_result: "உயிர்நாடி அறிகுறிகள் பகுப்பாய்வு",
    section_hospitals: "உங்கள் அருகிலுள்ள பரிந்துரைக்கப்பட்ட மருத்துவமனைகள்",
    hospitals_desc: "உங்கள் நிலைக்கு தேவையான நிபுணர் அடிப்படையில், அருகிலுள்ள மருத்துவமனைகள்:",
    detecting_location: "உங்கள் இருப்பிடத்தைக் கண்டறிகிறது...",
    lbl_patient_id: "உங்கள் நோயாளி ID", patient_id_note: "குறிப்புக்கு இந்த IDயை சேமிக்கவும்.",
    btn_new: "புதிய பரிசோதனை", btn_print: "அறிக்கை அச்சிடு",
    btn_directions: "வழிகளைப் பெறுங்கள்", btn_notify: "மருத்துவமனைக்கு தெரிவிக்கவும்",
    footer_text: "© 2026 NeuraX — AI-இயங்கும் தொலைநிலை சுகாதார தளம்", footer_hipaa: "HIPAA இணக்கம்",
    toast_analysis_done: "சுகாதார பகுப்பாய்வு முடிந்தது!", toast_notify_sent: "எச்சரிக்கை அனுப்பப்பட்டது!",
    matching_symptoms: "பொருந்தும் அறிகுறிகள்:", no_factors: "குறிப்பிடத்தக்க காரணிகள் கண்டறியப்படவில்லை.",
    no_disease: "குறிப்பிட்ட நிலைகளை தீர்மானிக்க முடியவில்லை.", loc_detected: "இருப்பிடம் கண்டறியப்பட்டது",
    loc_unavail: "இருப்பிடம் கிடைக்கவில்லை"
  },
  bn: {
    nav_home: "হোম", nav_patient: "রোগী পোর্টাল", nav_hospital: "হাসপাতাল পোর্টাল",
    nav_encrypted: "AES-256 এনক্রিপ্টেড", lang_label: "ভাষা",
    patient_title: "AI স্বাস্থ্য পরীক্ষা", patient_subtitle: "AI-চালিত স্বাস্থ্য ঝুঁকি বিশ্লেষণের জন্য আপনার তথ্য প্রদান করুন",
    section_info: "রোগীর তথ্য", lbl_name: "পুরো নাম", lbl_age: "বয়স",
    lbl_gender: "লিঙ্গ", lbl_location: "অবস্থান", lbl_contact: "যোগাযোগ নম্বর",
    ph_name: "আপনার পুরো নাম লিখুন", ph_age: "বয়স লিখুন",
    ph_location: "শহর বা গ্রাম", ph_contact: "ফোন নম্বর",
    opt_gender: "লিঙ্গ নির্বাচন করুন", opt_male: "পুরুষ", opt_female: "মহিলা", opt_other: "অন্য",
    section_symptoms: "আপনার উপসর্গ নির্বাচন করুন", symptoms_desc: "আপনি যে সব উপসর্গ অনুভব করছেন তাতে ক্লিক করুন",
    selected_count: "নির্বাচিত:", symptom_unit: "উপসর্গ",
    section_describe: "আপনার উপসর্গ বর্ণনা করুন",
    describe_text: "আপনার উপসর্গ সম্পর্কে বিস্তারিত লিখুন।",
    ph_describe: "যেমন, গত ৩ দিন ধরে মাথা ব্যথা হচ্ছে...",
    section_upload: "মেডিকেল ছবি আপলোড করুন (ঐচ্ছিক)",
    upload_desc: "ত্বকের সমস্যা, আঘাত, পরীক্ষার রিপোর্টের ছবি আপলোড করুন।",
    upload_drag: "এখানে ছবি টেনে আনুন", upload_or: "বা ফাইল ব্রাউজ করুন",
    upload_formats: "সমর্থিত: JPG, PNG, WEBP, PDF — সর্বোচ্চ 5MB",
    section_vitals: "গুরুত্বপূর্ণ পরামিতি",
    vitals_desc: "পাওয়া গেলে আপনার বর্তমান গুরুত্বপূর্ণ লক্ষণ প্রদান করুন।",
    lbl_hr: "হৃদস্পন্দন (BPM)", lbl_sbp: "সিস্টোলিক রক্তচাপ",
    lbl_dbp: "ডায়াস্টোলিক রক্তচাপ", lbl_temp: "শরীরের তাপমাত্রা (°F)",
    lbl_spo2: "SpO2 মাত্রা (%)", lbl_bmi: "BMI",
    btn_analyze: "স্বাস্থ্য ঝুঁকি বিশ্লেষণ করুন", btn_note: "আপনার ডেটা AI দ্বারা প্রক্রিয়াকৃত এবং এনক্রিপ্টেড",
    risk_score_label: "ঝুঁকি স্কোর", encrypted_result: "এনক্রিপ্টেড ফলাফল",
    section_disease: "সম্ভাব্য রোগ পূর্বাভাস", disease_desc: "আপনার উপসর্গের উপর ভিত্তি করে সম্ভাব্য অবস্থা:",
    section_risk: "ঝুঁকি মাত্রা বিশ্লেষণ", section_triage: "ট্রায়েজ শ্রেণীবিভাগ",
    section_factors: "অবদানকারী কারণ (XAI)", section_vitals_result: "গুরুত্বপূর্ণ লক্ষণ বিশ্লেষণ",
    section_hospitals: "কাছের প্রস্তাবিত হাসপাতাল",
    hospitals_desc: "আপনার অবস্থার জন্য প্রয়োজনীয় বিশেষজ্ঞের ভিত্তিতে কাছের হাসপাতাল:",
    detecting_location: "আপনার অবস্থান শনাক্ত করা হচ্ছে...",
    lbl_patient_id: "আপনার রোগী ID", patient_id_note: "এই ID সংরক্ষণ করুন।",
    btn_new: "নতুন পরীক্ষা", btn_print: "রিপোর্ট প্রিন্ট",
    btn_directions: "দিকনির্দেশ", btn_notify: "হাসপাতালকে জানান",
    footer_text: "© 2026 NeuraX — AI-চালিত দূরবর্তী স্বাস্থ্যসেবা প্ল্যাটফর্ম", footer_hipaa: "HIPAA অনুসারী",
    toast_analysis_done: "স্বাস্থ্য বিশ্লেষণ সম্পন্ন!", toast_notify_sent: "সতর্কতা পাঠানো হয়েছে!",
    matching_symptoms: "মিলে যাওয়া উপসর্গ:", no_factors: "কোনো গুরুত্বপূর্ণ কারণ পাওয়া যায়নি।",
    no_disease: "নির্দিষ্ট অবস্থা নির্ধারণ করা যায়নি।", loc_detected: "অবস্থান শনাক্ত হয়েছে",
    loc_unavail: "অবস্থান পাওয়া যায়নি"
  },
  mr: {
    nav_home: "मुख्यपृष्ठ", nav_patient: "रुग्ण पोर्टल", nav_hospital: "रुग्णालय पोर्टल",
    nav_encrypted: "AES-256 एन्क्रिप्टेड", lang_label: "भाषा",
    patient_title: "AI आरोग्य तपासणी", patient_subtitle: "AI-चालित आरोग्य जोखीम विश्लेषणासाठी तुमचे तपशील प्रविष्ट करा",
    section_info: "रुग्ण माहिती", lbl_name: "पूर्ण नाव", lbl_age: "वय",
    lbl_gender: "लिंग", lbl_location: "स्थान", lbl_contact: "संपर्क क्रमांक",
    ph_name: "तुमचे पूर्ण नाव प्रविष्ट करा", ph_age: "वय प्रविष्ट करा",
    ph_location: "शहर किंवा गाव", ph_contact: "फोन नंबर",
    opt_gender: "लिंग निवडा", opt_male: "पुरुष", opt_female: "स्त्री", opt_other: "इतर",
    section_symptoms: "तुमची लक्षणे निवडा", symptoms_desc: "तुम्हाला सध्या जाणवत असलेल्या सर्व लक्षणांवर क्लिक करा",
    selected_count: "निवडलेले:", symptom_unit: "लक्षणे",
    section_describe: "तुमच्या लक्षणांचे वर्णन करा",
    describe_text: "तुमच्या लक्षणांबद्दल तपशीलवार लिहा.",
    ph_describe: "उदा., मला गेल्या ३ दिवसांपासून तीव्र डोकेदुखी आहे...",
    section_upload: "वैद्यकीय प्रतिमा अपलोड करा (ऐच्छिक)",
    upload_desc: "त्वचेच्या स्थिती, दुखापती, चाचणी अहवाल यांचे फोटो अपलोड करा.",
    upload_drag: "प्रतिमा येथे ड्रॅग करा", upload_or: "किंवा फाइल्स ब्राउझ करा",
    upload_formats: "समर्थित: JPG, PNG, WEBP, PDF — फाइलमागे कमाल 5MB",
    section_vitals: "महत्त्वाचे मापदंड",
    vitals_desc: "उपलब्ध असल्यास तुमचे सध्याचे महत्त्वाचे चिन्हे प्रविष्ट करा.",
    lbl_hr: "हृदय गती (BPM)", lbl_sbp: "सिस्टोलिक रक्तदाब",
    lbl_dbp: "डायस्टोलिक रक्तदाब", lbl_temp: "शरीराचे तापमान (°F)",
    lbl_spo2: "SpO2 पातळी (%)", lbl_bmi: "BMI",
    btn_analyze: "आरोग्य जोखीम विश्लेषण करा", btn_note: "तुमचा डेटा AI मॉडेलद्वारे प्रक्रिया केला जातो",
    risk_score_label: "जोखीम स्कोर", encrypted_result: "एन्क्रिप्टेड निकाल",
    section_disease: "संभाव्य रोग अंदाज", disease_desc: "तुमच्या लक्षणांवर आधारित संभाव्य स्थिती:",
    section_risk: "जोखीम पातळी विश्लेषण", section_triage: "ट्रायेज वर्गीकरण",
    section_factors: "योगदान घटक (XAI)", section_vitals_result: "महत्त्वाची चिन्हे विश्लेषण",
    section_hospitals: "तुमच्या जवळील शिफारस केलेली रुग्णालये",
    hospitals_desc: "तुमच्या स्थितीसाठी आवश्यक तज्ञांवर आधारित जवळची रुग्णालये:",
    detecting_location: "तुमचे स्थान शोधत आहे...",
    lbl_patient_id: "तुमची रुग्ण ID", patient_id_note: "संदर्भासाठी ही ID जतन करा.",
    btn_new: "नवीन तपासणी", btn_print: "अहवाल छापा",
    btn_directions: "दिशानिर्देश मिळवा", btn_notify: "रुग्णालयाला कळवा",
    footer_text: "© 2026 NeuraX — AI-चालित दूरस्थ आरोग्य सेवा व्यासपीठ", footer_hipaa: "HIPAA अनुपालन",
    toast_analysis_done: "आरोग्य विश्लेषण पूर्ण!", toast_notify_sent: "सूचना पाठवली!",
    matching_symptoms: "जुळणारी लक्षणे:", no_factors: "कोणतेही महत्त्वाचे घटक आढळले नाहीत.",
    no_disease: "विशिष्ट स्थिती निश्चित करता आली नाही.", loc_detected: "स्थान ओळखले",
    loc_unavail: "स्थान अनुपलब्ध"
  }
};

// Symptom translations
const SYMPTOM_TRANSLATIONS = {
  en: { fever: "Fever", cough: "Cough", headache: "Headache", fatigue: "Fatigue", shortness_of_breath: "Shortness of Breath", chest_pain: "Chest Pain", nausea: "Nausea", vomiting: "Vomiting", diarrhea: "Diarrhea", body_ache: "Body Ache", sore_throat: "Sore Throat", runny_nose: "Runny Nose", dizziness: "Dizziness", abdominal_pain: "Abdominal Pain", loss_of_appetite: "Loss of Appetite", skin_rash: "Skin Rash", joint_pain: "Joint Pain", blurred_vision: "Blurred Vision", frequent_urination: "Frequent Urination", weight_loss: "Weight Loss", swelling: "Swelling", numbness: "Numbness/Tingling", confusion: "Confusion", rapid_heartbeat: "Rapid Heartbeat", excessive_thirst: "Excessive Thirst" },
  hi: { fever: "बुखार", cough: "खांसी", headache: "सिरदर्द", fatigue: "थकान", shortness_of_breath: "सांस की तकलीफ", chest_pain: "छाती में दर्द", nausea: "मतली", vomiting: "उल्टी", diarrhea: "दस्त", body_ache: "शरीर दर्द", sore_throat: "गले में खराश", runny_nose: "बहती नाक", dizziness: "चक्कर आना", abdominal_pain: "पेट दर्द", loss_of_appetite: "भूख न लगना", skin_rash: "त्वचा पर दाने", joint_pain: "जोड़ों का दर्द", blurred_vision: "धुंधली दृष्टि", frequent_urination: "बार-बार पेशाब", weight_loss: "वजन घटना", swelling: "सूजन", numbness: "सुन्नपन", confusion: "भ्रम", rapid_heartbeat: "तेज़ धड़कन", excessive_thirst: "अत्यधिक प्यास" },
  te: { fever: "జ్వరం", cough: "దగ్గు", headache: "తలనొప్పి", fatigue: "అలసట", shortness_of_breath: "ఊపిరి ఆడకపోవడం", chest_pain: "ఛాతీ నొప్పి", nausea: "వికారం", vomiting: "వాంతి", diarrhea: "అతిసారం", body_ache: "ఒళ్ళు నొప్పి", sore_throat: "గొంతు నొప్పి", runny_nose: "ముక్కు కారడం", dizziness: "తల తిరగడం", abdominal_pain: "కడుపు నొప్పి", loss_of_appetite: "ఆకలి మందగించడం", skin_rash: "చర్మ దద్దుర్లు", joint_pain: "కీళ్ల నొప్పి", blurred_vision: "అస్పష్ట దృష్టి", frequent_urination: "తరచుగా మూత్ర విసర్జన", weight_loss: "బరువు తగ్గడం", swelling: "వాపు", numbness: "తిమ్మిరి", confusion: "గందరగోళం", rapid_heartbeat: "వేగంగా గుండె కొట్టుకోవడం", excessive_thirst: "అతిగా దాహం" },
  ta: { fever: "காய்ச்சல்", cough: "இருமல்", headache: "தலைவலி", fatigue: "சோர்வு", shortness_of_breath: "மூச்சுத்திணறல்", chest_pain: "மார்பு வலி", nausea: "குமட்டல்", vomiting: "வாந்தி", diarrhea: "வயிற்றுப்போக்கு", body_ache: "உடல் வலி", sore_throat: "தொண்டை வலி", runny_nose: "மூக்கு ஒழுகுதல்", dizziness: "தலைச்சுற்றல்", abdominal_pain: "வயிற்று வலி", loss_of_appetite: "பசியின்மை", skin_rash: "தோல் அரிப்பு", joint_pain: "மூட்டு வலி", blurred_vision: "மங்கலான பார்வை", frequent_urination: "அடிக்கடி சிறுநீர்", weight_loss: "எடை இழப்பு", swelling: "வீக்கம்", numbness: "உணர்வின்மை", confusion: "குழப்பம்", rapid_heartbeat: "விரைவான இதயத் துடிப்பு", excessive_thirst: "அதிக தாகம்" },
  bn: { fever: "জ্বর", cough: "কাশি", headache: "মাথাব্যথা", fatigue: "ক্লান্তি", shortness_of_breath: "শ্বাসকষ্ট", chest_pain: "বুকে ব্যথা", nausea: "বমি বমি ভাব", vomiting: "বমি", diarrhea: "ডায়রিয়া", body_ache: "শরীর ব্যথা", sore_throat: "গলা ব্যথা", runny_nose: "নাক দিয়ে পানি পড়া", dizziness: "মাথা ঘোরা", abdominal_pain: "পেট ব্যথা", loss_of_appetite: "ক্ষুধামন্দা", skin_rash: "ত্বকে ফুসকুড়ি", joint_pain: "জয়েন্টে ব্যথা", blurred_vision: "ঝাপসা দৃষ্টি", frequent_urination: "ঘন ঘন প্রস্রাব", weight_loss: "ওজন হ্রাস", swelling: "ফোলা", numbness: "অসাড়তা", confusion: "বিভ্রান্তি", rapid_heartbeat: "দ্রুত হৃদস্পন্দন", excessive_thirst: "অতিরিক্ত তৃষ্ণা" },
  mr: { fever: "ताप", cough: "खोकला", headache: "डोकेदुखी", fatigue: "थकवा", shortness_of_breath: "श्वास लागणे", chest_pain: "छातीत दुखणे", nausea: "मळमळ", vomiting: "उलटी", diarrhea: "जुलाब", body_ache: "अंगदुखी", sore_throat: "घसा दुखणे", runny_nose: "नाक वाहणे", dizziness: "चक्कर येणे", abdominal_pain: "पोटदुखी", loss_of_appetite: "भूक न लागणे", skin_rash: "त्वचेवर पुरळ", joint_pain: "सांधेदुखी", blurred_vision: "अंधुक दृष्टी", frequent_urination: "वारंवार लघवी", weight_loss: "वजन कमी होणे", swelling: "सूज", numbness: "बधिरपणा", confusion: "गोंधळ", rapid_heartbeat: "जलद हृदयाचे ठोके", excessive_thirst: "अती तहान" }
};

const LANG_NAMES = {
  en: "English", hi: "हिन्दी", te: "తెలుగు",
  ta: "தமிழ்", bn: "বাংলা", mr: "मराठी"
};

let currentLang = localStorage.getItem('neurax_lang') || 'en';

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('neurax_lang', lang);
  applyTranslations();
  translateSymptomChips();
  // Update lang selector display
  const sel = document.getElementById('langSelect');
  if (sel) sel.value = lang;
}

function t(key) {
  return (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) || TRANSLATIONS.en[key] || key;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const text = t(key);
    if (text) el.textContent = text;
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    const text = t(key);
    if (text) el.setAttribute('placeholder', text);
  });
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const key = el.getAttribute('data-i18n-html');
    const text = t(key);
    if (text) el.innerHTML = text;
  });
}

function translateSymptomChips() {
  const chips = document.querySelectorAll('.symptom-chip');
  const symTrans = SYMPTOM_TRANSLATIONS[currentLang] || SYMPTOM_TRANSLATIONS.en;
  chips.forEach(chip => {
    const key = chip.getAttribute('data-symptom');
    if (key && symTrans[key]) {
      chip.textContent = symTrans[key];
    }
  });
}
