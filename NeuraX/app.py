"""
NeuraX - AI-Powered Remote Healthcare Platform
Flask Backend API
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ml_model import (
    load_models, predict_health_risk, train_models,
    SYMPTOM_LIST, SYMPTOM_DISPLAY_NAMES, predict_diseases
)
import json
import math
import os
import uuid
import random
import smtplib
from email.message import EmailMessage
from datetime import datetime
import hashlib
import requests as http_requests

app = Flask(__name__)
CORS(app)

# --- EMAIL OTP CONFIGURATION ---
# These will be loaded from Vercel environment variables or local .env
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Temporary storage for OTPs (in-memory)
# Format: { "email@example.com": "123456" }
otp_storage = {}

# Upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB max total
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load ML models
risk_model, triage_model = load_models()

# In-memory database — starts empty, fills with real patient submissions
patients_db = {}
hospital_patients = []


# ====== Page Routes ======

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/patient")
def patient_dashboard():
    return render_template("patient_dashboard.html")


@app.route("/hospital")
def hospital_dashboard():
    return render_template("hospital_dashboard.html")

@app.route("/hospital_auth")
def hospital_auth():
    return render_template("hospital_auth.html")

@app.route("/doctor_auth")
def doctor_auth():
    return render_template("doctor_auth.html")

@app.route("/doctor_dashboard")
def doctor_dashboard():
    return render_template("doctor_dashboard.html")
# ====== File serving ======

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ====== API Routes ======

@app.route("/api/symptoms", methods=["GET"])
def get_symptoms():
    """Return available symptoms list."""
    symptoms = [
        {"key": s, "display_name": SYMPTOM_DISPLAY_NAMES.get(s, s)}
        for s in SYMPTOM_LIST
    ]
    return jsonify({"symptoms": symptoms})


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Predict health risk, triage, and possible diseases for patient data.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        required = ["age", "gender", "symptoms", "vitals"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Track which vitals were actually entered by user
        entered_vitals = data.get("entered_vitals", [])

        # Run prediction
        result = predict_health_risk(data, risk_model, triage_model)

        # Filter vital_analysis to only show user-entered vitals
        if entered_vitals:
            result["vital_analysis"] = [
                v for v in result["vital_analysis"]
                if v["name"].lower().replace(" ", "_") in entered_vitals
                or v["name"] in [VITAL_FIELD_MAP.get(ev, ev) for ev in entered_vitals]
            ]
        else:
            result["vital_analysis"] = []

        # Predict possible diseases
        disease_predictions = predict_diseases(data.get("symptoms", []))
        result["disease_predictions"] = disease_predictions

        # Get unique specialists needed
        specialists_needed = list(set(d["specialist"] for d in disease_predictions))
        result["specialists_needed"] = specialists_needed

        # Store patient record
        patient_id = str(uuid.uuid4())[:8]
        patient_record = {
            "id": patient_id,
            "name": data.get("name", "Anonymous"),
            "age": data["age"],
            "gender": data["gender"],
            "symptoms": data["symptoms"],
            "symptom_description": data.get("symptom_description", ""),
            "uploaded_images": data.get("uploaded_images", []),
            "vitals": data["vitals"],
            "risk_level": result["risk_level"],
            "triage": result["triage"],
            "risk_score": result["risk_score"],
            "disease_predictions": disease_predictions,
            "timestamp": datetime.now().isoformat(),
            "status": "Pending",
            "location": data.get("location", "Unknown"),
            "contact": data.get("contact", "N/A")
        }
        patients_db[patient_id] = patient_record
        hospital_patients.append(patient_record)

        result["patient_id"] = patient_id
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/patients", methods=["GET"])
def get_patients():
    """Return all patients for hospital dashboard."""
    return jsonify({
        "patients": hospital_patients,
        "stats": get_dashboard_stats()
    })


@app.route("/api/patients/<patient_id>/status", methods=["PUT"])
def update_patient_status(patient_id):
    """Update patient status."""
    data = request.get_json()
    new_status = data.get("status", "Pending")
    doctor_id = data.get("doctor_id")
    doctor_name = data.get("doctor_name")

    for patient in hospital_patients:
        if patient["id"] == patient_id:
            patient["status"] = new_status
            if doctor_id:
                patient["assigned_doctor_id"] = doctor_id
            if doctor_name:
                patient["assigned_doctor_name"] = doctor_name
            return jsonify({"success": True, "patient": patient})

    return jsonify({"error": "Patient not found"}), 404


@app.route("/api/upload-images", methods=["POST"])
def upload_images():
    """Upload patient medical images."""
    try:
        if 'images' not in request.files:
            return jsonify({"error": "No images provided"}), 400

        files = request.files.getlist('images')
        saved_files = []

        for file in files:
            if file and file.filename and allowed_file(file.filename):
                # Create unique filename
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_name = f"{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                file.save(filepath)
                saved_files.append(unique_name)

        return jsonify({"files": saved_files, "count": len(saved_files)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/dashboard/stats", methods=["GET"])
def dashboard_stats():
    """Return dashboard statistics."""
    return jsonify(get_dashboard_stats())


# Vital field name mapping for filtering
VITAL_FIELD_MAP = {
    "heart_rate": "Heart Rate",
    "systolic_bp": "Systolic BP",
    "diastolic_bp": "Diastolic BP",
    "temperature": "Temperature",
    "spo2": "SpO2",
    "bmi": "BMI"
}


# Notification log
notifications_log = []


def geocode_location(location_name):
    """Geocode a location name to lat/lng using OpenStreetMap Nominatim (free, no API key)."""
    try:
        resp = http_requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": location_name, "format": "json", "limit": 1, "countrycodes": "in"},
            headers={"User-Agent": "NeuraX-Healthcare/1.0"},
            timeout=8
        )
        results = resp.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None


def search_real_hospitals(lat, lng, radius_km=30):
    """Search for real hospitals near a location using OpenStreetMap Overpass API (free, no API key)."""
    radius_m = int(radius_km * 1000)
    overpass_query = f"""
    [out:json][timeout:15];
    (
      node["amenity"="hospital"](around:{radius_m},{lat},{lng});
      way["amenity"="hospital"](around:{radius_m},{lat},{lng});
      relation["amenity"="hospital"](around:{radius_m},{lat},{lng});
      node["amenity"="clinic"](around:{radius_m},{lat},{lng});
      way["amenity"="clinic"](around:{radius_m},{lat},{lng});
    );
    out center body;
    """
    try:
        resp = http_requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": overpass_query},
            timeout=15
        )
        data = resp.json()
        hospitals = []
        seen_names = set()

        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name", tags.get("name:en", "")).strip()
            if not name or name.lower() in seen_names:
                continue
            seen_names.add(name.lower())

            # Get coordinates (node vs way/relation center)
            h_lat = element.get("lat") or element.get("center", {}).get("lat")
            h_lng = element.get("lon") or element.get("center", {}).get("lon")
            if not h_lat or not h_lng:
                continue

            amenity_type = tags.get("amenity", "hospital")
            healthcare = tags.get("healthcare", "")
            operator_type = tags.get("operator:type", tags.get("ownership", "")).lower()
            h_type = "Government" if any(k in operator_type for k in ["government", "public", "state"]) else "Private" if any(k in operator_type for k in ["private", "corporate"]) else "Hospital"

            phone = tags.get("phone", tags.get("contact:phone", "N/A"))
            beds = tags.get("beds", "N/A")
            website = tags.get("website", tags.get("contact:website", ""))
            addr_city = tags.get("addr:city", tags.get("addr:district", ""))
            addr_full = tags.get("addr:full", "")
            city = addr_city or addr_full or ""

            # Build specialty list from tags
            specialties_tags = tags.get("healthcare:speciality", tags.get("health_specialty", ""))
            specialties = [s.strip().title() for s in specialties_tags.split(";") if s.strip()] if specialties_tags else ["General Physician"]

            distance = round(haversine(lat, lng, h_lat, h_lng), 1)

            hospitals.append({
                "id": f"osm_{element.get('id', '')}",
                "name": name,
                "lat": h_lat,
                "lng": h_lng,
                "city": city,
                "specialties": specialties,
                "phone": phone,
                "type": h_type,
                "beds": beds,
                "website": website,
                "distance_km": distance,
                "amenity": amenity_type
            })

        # Sort by distance
        hospitals.sort(key=lambda x: x["distance_km"])
        return hospitals[:15]

    except Exception as e:
        print(f"Overpass API error: {e}")
        return []


@app.route("/api/hospitals/search", methods=["POST"])
def search_hospitals():
    """Search for real nearby hospitals using OpenStreetMap Overpass API."""
    try:
        data = request.get_json()
        specialties = data.get("specialties", [])
        user_lat = data.get("lat")
        user_lng = data.get("lng")
        location_name = data.get("location", "")
        radius_km = data.get("radius_km", 30)

        # If no coordinates but have location name, geocode it
        if (not user_lat or not user_lng) and location_name:
            user_lat, user_lng = geocode_location(location_name)

        if not user_lat or not user_lng:
            return jsonify({"hospitals": [], "error": "Could not determine location. Please enable GPS or enter a valid location."})

        # Search for real hospitals via Overpass API
        hospitals = search_real_hospitals(user_lat, user_lng, radius_km)

        # If very few results, expand search radius
        if len(hospitals) < 3 and radius_km < 80:
            hospitals = search_real_hospitals(user_lat, user_lng, 80)

        # Attach matched specialties
        for h in hospitals:
            if specialties:
                matched = [s for s in specialties if s in h["specialties"]]
                h["matched_specialties"] = matched if matched else ["General Physician"]
            else:
                h["matched_specialties"] = h["specialties"]

        return jsonify({"hospitals": hospitals})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/hospitals/<hospital_id>/notify", methods=["POST"])
def notify_hospital(hospital_id):
    """Send notification to a hospital about an incoming patient."""
    try:
        data = request.get_json()
        patient_name = data.get("patient_name", "Unknown")
        patient_id = data.get("patient_id", "N/A")
        disease = data.get("disease", "Not specified")
        risk_level = data.get("risk_level", "Unknown")
        triage = data.get("triage", "Unknown")
        hospital_name = data.get("hospital_name", "Hospital")

        # Create notification record
        notification = {
            "id": str(uuid.uuid4())[:8],
            "hospital_id": hospital_id,
            "hospital_name": hospital_name,
            "patient_name": patient_name,
            "patient_id": patient_id,
            "disease": disease,
            "risk_level": risk_level,
            "triage": triage,
            "timestamp": datetime.now().isoformat(),
            "status": "Sent"
        }
        notifications_log.append(notification)

        return jsonify({
            "success": True,
            "message": f"Notification sent to {hospital_name}",
            "notification": notification
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/geocode", methods=["POST"])
def geocode():
    """Geocode a location name to coordinates."""
    try:
        data = request.get_json()
        location = data.get("location", "")
        if not location:
            return jsonify({"error": "No location provided"}), 400
        lat, lng = geocode_location(location)
        if lat and lng:
            return jsonify({"lat": lat, "lng": lng, "location": location})
        return jsonify({"error": "Location not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/send-otp", methods=["POST"])
def send_otp():
    """Generate and send an OTP to an email address."""
    try:
        data = request.get_json()
        email_addr = data.get("email")
        
        if not email_addr:
            return jsonify({"error": "Email address is required"}), 400
            
        # Generate a 6-digit random OTP
        otp = str(random.randint(100000, 999999))
        
        # In a generic situation we save it locally in the memory dict
        otp_storage[email_addr] = otp
        
        # Setup email
        msg = EmailMessage()
        msg['Subject'] = 'Your NeuraX Verification Code'
        msg['From'] = SENDER_EMAIL
        msg['To'] = email_addr
        msg.set_content(f"""
        Hello!
        
        Thank you for registering at NeuraX.
        Your email verification code is: {otp}
        
        Please enter this code on the registration page to verify your account.
        This code is valid for your current session.
        """)
        
        # Send Email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
            
        return jsonify({"success": True, "message": "OTP sent successfully"})
        
    except Exception as e:
        print("OTP Send Error:", e)
        return jsonify({"error": "Failed to send OTP. Ensure your email and app password are correct in app.py"}), 500


@app.route("/api/verify-otp", methods=["POST"])
def verify_otp():
    """Check if the provided OTP matches the email."""
    try:
        data = request.get_json()
        email_addr = data.get("email")
        user_otp = data.get("otp")
        
        if not email_addr or not user_otp:
            return jsonify({"error": "Email and OTP are required"}), 400
            
        stored_otp = otp_storage.get(email_addr)
        
        if stored_otp and stored_otp == user_otp:
            # OTP is correct! Delete it to prevent reuse
            del otp_storage[email_addr]
            return jsonify({"success": True, "message": "Email verified successfully"})
        else:
            return jsonify({"error": "Invalid or expired OTP"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on Earth."""
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def get_dashboard_stats():
    """Calculate dashboard statistics."""
    total = len(hospital_patients)
    emergency = sum(1 for p in hospital_patients if p["triage"] == "Emergency")
    urgent = sum(1 for p in hospital_patients if p["triage"] == "Urgent")
    routine = sum(1 for p in hospital_patients if p["triage"] == "Routine")

    pending = sum(1 for p in hospital_patients if p["status"] == "Pending")
    under_review = sum(1 for p in hospital_patients if p["status"] == "Under Review")
    assigned = sum(1 for p in hospital_patients if p["status"] == "Assigned")
    completed = sum(1 for p in hospital_patients if p["status"] == "Completed")

    high_risk = sum(1 for p in hospital_patients if p["risk_level"] == "High")
    medium_risk = sum(1 for p in hospital_patients if p["risk_level"] == "Medium")
    low_risk = sum(1 for p in hospital_patients if p["risk_level"] == "Low")

    return {
        "total_patients": total,
        "emergency": emergency,
        "urgent": urgent,
        "routine": routine,
        "pending": pending,
        "under_review": under_review,
        "assigned": assigned,
        "completed": completed,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "avg_risk_score": round(
            sum(p.get("risk_score", 0) for p in hospital_patients) / max(total, 1), 1
        )
    }

@app.route("/api/ai-chat", methods=["POST"])
def ai_chat():
    """Talks to Groq AI to ask questions and extract patient details."""
    data = request.get_json()
    history = data.get("history", [])
    lang = data.get("lang", "en")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return jsonify({"reply": "Backend error: GROQ_API_KEY is not configured in the environment variables. The AI cannot respond without it."})

    # Instruct the AI
    system_prompt = f"""You are a helpful, empathetic medical voice assistant. 
The user is speaking in language code '{lang}'. ALWAYS ask questions and reply in '{lang}'.
Your goal is to extract strictly 4 pieces of information:
1. Patient's Full Name
2. Age (number)
3. Gender (Male/Female/Other)
4. Their symptoms 

Current chat history is provided. If any of the above 4 details are missing, ASK the patient for the missing information in a friendly, conversational way in '{lang}'. DO NOT output JSON if you are asking a question.

Once you have ALL the required info, DO NOT ask another question. Instead, output ONLY a valid JSON object starting with {{ "status": "complete" }} and NOTHING ELSE. No backticks, no code blocks, just pure JSON.
The JSON format must be EXACTLY:
{{
  "status": "complete",
  "patientData": {{
    "name": "extracted name",
    "age": age,
    "gender": "male or female or other",
    "symptoms": ["headache", "fever", etc map to closest standard symptom],
    "description": "Any additional context they provided"
  }}
}}"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    
    for msg in history:
        if "role" in msg and "parts" in msg:
            # Map frontend history format to OpenAI format
            role = "assistant" if msg["role"] == "model" else "user"
            messages.append({"role": role, "content": msg["parts"]})
            
    payload = {
        "model": "llama3-70b-8192",
        "messages": messages,
        "temperature": 0.2
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        res = http_requests.post(url, json=payload, headers=headers, timeout=10)
        res_data = res.json()
        
        if res.status_code != 200:
            print("Groq API Error:", res_data)
            return jsonify({"reply": "I am having trouble connecting to the AI brain. Please try again later."})
            
        reply_text = res_data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Check if the AI outputted a JSON object
        clean_text = reply_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:-3].strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:-3].strip()
            
        if clean_text.startswith("{") and '"status"' in clean_text:
            try:
                parsed = json.loads(clean_text)
                return jsonify(parsed)
            except json.JSONDecodeError:
                pass
                
        return jsonify({"status": "asking", "reply": reply_text})
    except Exception as e:
        print("Chat exception:", e)
        return jsonify({"reply": "Network error with AI provider."})

@app.route("/api/ai-chat/translate", methods=["POST"])
def ai_translate():
    """Translates the diagnosis text back to the user's spoken language."""
    data = request.get_json()
    text = data.get("text", "")
    target_lang = data.get("target_lang", "en")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return jsonify({"translated_text": text})
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    prompt = f"Translate the following medical triage result into the language corresponding to code '{target_lang}'. Return ONLY the translated text, nothing else.\n\nText: {text}"
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        res = http_requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code == 200:
            reply_text = res.json().get("choices", [{}])[0].get("message", {}).get("content", text)
            return jsonify({"translated_text": reply_text.strip()})
    except:
        pass
        
    return jsonify({"translated_text": text})


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  NeuraX - AI-Powered Remote Healthcare Platform")
    print("=" * 60)
    print("  [*] Landing Page:        http://localhost:5000")
    print("  [+] Patient Dashboard:   http://localhost:5000/patient")
    print("  [+] Hospital Dashboard:  http://localhost:5000/hospital")
    print("=" * 60 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
