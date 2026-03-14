"""
NeuraX - AI Health Risk Prediction Model
Uses Random Forest Classifier for health risk prediction and triage classification.
Includes Explainable AI via feature importance analysis.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import json

# Symptom mapping - comprehensive list
SYMPTOM_LIST = [
    "fever", "cough", "headache", "fatigue", "shortness_of_breath",
    "chest_pain", "nausea", "vomiting", "diarrhea", "body_ache",
    "sore_throat", "runny_nose", "dizziness", "abdominal_pain",
    "loss_of_appetite", "skin_rash", "joint_pain", "blurred_vision",
    "frequent_urination", "weight_loss", "swelling", "numbness",
    "confusion", "rapid_heartbeat", "excessive_thirst"
]

SYMPTOM_DISPLAY_NAMES = {
    "fever": "Fever", "cough": "Cough", "headache": "Headache",
    "fatigue": "Fatigue", "shortness_of_breath": "Shortness of Breath",
    "chest_pain": "Chest Pain", "nausea": "Nausea", "vomiting": "Vomiting",
    "diarrhea": "Diarrhea", "body_ache": "Body Ache",
    "sore_throat": "Sore Throat", "runny_nose": "Runny Nose",
    "dizziness": "Dizziness", "abdominal_pain": "Abdominal Pain",
    "loss_of_appetite": "Loss of Appetite", "skin_rash": "Skin Rash",
    "joint_pain": "Joint Pain", "blurred_vision": "Blurred Vision",
    "frequent_urination": "Frequent Urination", "weight_loss": "Weight Loss",
    "swelling": "Swelling", "numbness": "Numbness/Tingling",
    "confusion": "Confusion", "rapid_heartbeat": "Rapid Heartbeat",
    "excessive_thirst": "Excessive Thirst"
}

# Vital parameter ranges for risk scoring
VITAL_RANGES = {
    "heart_rate": {"normal": (60, 100), "warning": (50, 120), "critical": (0, 200)},
    "systolic_bp": {"normal": (90, 120), "warning": (80, 140), "critical": (0, 200)},
    "diastolic_bp": {"normal": (60, 80), "warning": (50, 90), "critical": (0, 130)},
    "temperature": {"normal": (97.0, 99.0), "warning": (96.0, 101.0), "critical": (94.0, 106.0)},
    "spo2": {"normal": (95, 100), "warning": (90, 100), "critical": (0, 100)},
    "bmi": {"normal": (18.5, 24.9), "warning": (16.0, 30.0), "critical": (0.0, 50.0)}
}


def generate_synthetic_data(n_samples=2000):
    """Generate synthetic patient data for training the model."""
    np.random.seed(42)
    data = []

    for _ in range(n_samples):
        # Random demographics
        age = np.random.randint(5, 90)
        gender = np.random.choice([0, 1])  # 0=Female, 1=Male

        # Generate symptoms (binary)
        n_symptoms = np.random.randint(0, 10)
        symptom_indices = np.random.choice(len(SYMPTOM_LIST), size=n_symptoms, replace=False)
        symptoms = [0] * len(SYMPTOM_LIST)
        for idx in symptom_indices:
            symptoms[idx] = 1

        # Generate vitals with some correlation to symptoms
        severity_factor = n_symptoms / 10.0

        heart_rate = np.random.normal(75 + severity_factor * 30, 15)
        systolic_bp = np.random.normal(120 + severity_factor * 20, 15)
        diastolic_bp = np.random.normal(80 + severity_factor * 10, 10)
        temperature = np.random.normal(98.6 + symptoms[0] * 2.0 + severity_factor * 0.5, 0.8)
        spo2 = np.random.normal(97 - severity_factor * 5, 2)
        bmi = np.random.normal(24, 5)

        # Clamp values
        heart_rate = np.clip(heart_rate, 40, 180)
        systolic_bp = np.clip(systolic_bp, 70, 200)
        diastolic_bp = np.clip(diastolic_bp, 40, 130)
        temperature = np.clip(temperature, 95, 106)
        spo2 = np.clip(spo2, 70, 100)
        bmi = np.clip(bmi, 12, 50)

        # Calculate risk score
        risk_score = 0

        # Symptom-based risk scoring
        critical_symptoms = [symptoms[4], symptoms[5], symptoms[22], symptoms[23]]  # shortness of breath, chest pain, confusion, rapid heartbeat
        moderate_symptoms = [symptoms[0], symptoms[6], symptoms[7], symptoms[12], symptoms[17]]  # fever, nausea, vomiting, dizziness, blurred vision

        risk_score += sum(critical_symptoms) * 3
        risk_score += sum(moderate_symptoms) * 1.5
        risk_score += (n_symptoms - sum(critical_symptoms) - sum(moderate_symptoms)) * 0.5

        # Vital-based risk scoring
        if heart_rate > 120 or heart_rate < 50:
            risk_score += 3
        elif heart_rate > 100 or heart_rate < 60:
            risk_score += 1

        if systolic_bp > 160 or systolic_bp < 80:
            risk_score += 3
        elif systolic_bp > 140 or systolic_bp < 90:
            risk_score += 1.5

        if temperature > 103:
            risk_score += 3
        elif temperature > 100:
            risk_score += 1.5

        if spo2 < 90:
            risk_score += 4
        elif spo2 < 95:
            risk_score += 2

        # Age risk factor
        if age > 65 or age < 10:
            risk_score += 1.5

        # Determine risk level
        if risk_score >= 8:
            risk_level = 2  # High
            triage = 0  # Emergency
        elif risk_score >= 4:
            risk_level = 1  # Medium
            triage = 1  # Urgent
        else:
            risk_level = 0  # Low
            triage = 2  # Routine

        row = [age, gender] + symptoms + [
            round(heart_rate, 1), round(systolic_bp, 1), round(diastolic_bp, 1),
            round(temperature, 1), round(spo2, 1), round(bmi, 1),
            risk_level, triage
        ]
        data.append(row)

    columns = ["age", "gender"] + SYMPTOM_LIST + [
        "heart_rate", "systolic_bp", "diastolic_bp",
        "temperature", "spo2", "bmi",
        "risk_level", "triage"
    ]

    return pd.DataFrame(data, columns=columns)


def train_models():
    """Train Random Forest models for risk prediction and triage classification."""
    print("Generating synthetic training data...")
    df = generate_synthetic_data(3000)

    feature_cols = ["age", "gender"] + SYMPTOM_LIST + [
        "heart_rate", "systolic_bp", "diastolic_bp",
        "temperature", "spo2", "bmi"
    ]
    X = df[feature_cols]

    # Risk Level Model
    y_risk = df["risk_level"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_risk, test_size=0.2, random_state=42)

    risk_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=12)
    risk_model.fit(X_train, y_train)
    risk_accuracy = risk_model.score(X_test, y_test)
    print(f"Risk Model Accuracy: {risk_accuracy:.4f}")

    # Triage Model
    y_triage = df["triage"]
    X_train, X_test, y_train, y_test = train_test_split(X, y_triage, test_size=0.2, random_state=42)

    triage_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=12)
    triage_model.fit(X_train, y_train)
    triage_accuracy = triage_model.score(X_test, y_test)
    print(f"Triage Model Accuracy: {triage_accuracy:.4f}")

    # Save models
    os.makedirs("models", exist_ok=True)
    joblib.dump(risk_model, "models/risk_model.pkl")
    joblib.dump(triage_model, "models/triage_model.pkl")

    # Save feature importances
    feature_importance = {
        "risk": dict(zip(feature_cols, risk_model.feature_importances_.tolist())),
        "triage": dict(zip(feature_cols, triage_model.feature_importances_.tolist()))
    }
    with open("models/feature_importance.json", "w") as f:
        json.dump(feature_importance, f, indent=2)

    print("Models saved successfully!")
    return risk_model, triage_model


def load_models():
    """Load trained models from disk."""
    if not os.path.exists("models/risk_model.pkl"):
        print("Models not found. Training new models...")
        return train_models()

    risk_model = joblib.load("models/risk_model.pkl")
    triage_model = joblib.load("models/triage_model.pkl")
    return risk_model, triage_model


def predict_health_risk(patient_data, risk_model, triage_model):
    """
    Predict health risk and triage level for a patient.
    
    patient_data: dict with keys: age, gender, symptoms (list), vitals (dict)
    Returns: prediction dict with risk_level, triage, confidence, explanations
    """
    feature_cols = ["age", "gender"] + SYMPTOM_LIST + [
        "heart_rate", "systolic_bp", "diastolic_bp",
        "temperature", "spo2", "bmi"
    ]

    # Build feature vector
    features = [0] * len(feature_cols)
    features[0] = patient_data.get("age", 30)
    features[1] = 1 if patient_data.get("gender", "male").lower() == "male" else 0

    # Set symptom features
    selected_symptoms = patient_data.get("symptoms", [])
    for symptom in selected_symptoms:
        if symptom in SYMPTOM_LIST:
            idx = SYMPTOM_LIST.index(symptom) + 2  # offset for age, gender
            features[idx] = 1

    # Set vital features
    vitals = patient_data.get("vitals", {})
    vital_offset = 2 + len(SYMPTOM_LIST)
    features[vital_offset] = vitals.get("heart_rate", 75)
    features[vital_offset + 1] = vitals.get("systolic_bp", 120)
    features[vital_offset + 2] = vitals.get("diastolic_bp", 80)
    features[vital_offset + 3] = vitals.get("temperature", 98.6)
    features[vital_offset + 4] = vitals.get("spo2", 97)
    features[vital_offset + 5] = vitals.get("bmi", 24)

    X = np.array(features).reshape(1, -1)

    # Predictions
    risk_pred = risk_model.predict(X)[0]
    risk_proba = risk_model.predict_proba(X)[0]
    triage_pred = triage_model.predict(X)[0]
    triage_proba = triage_model.predict_proba(X)[0]

    risk_labels = ["Low", "Medium", "High"]
    triage_labels = ["Emergency", "Urgent", "Routine"]

    # Explainable AI - Feature importance for this prediction
    risk_importances = risk_model.feature_importances_
    top_factors = []
    feature_contributions = []

    for i, (col, imp) in enumerate(zip(feature_cols, risk_importances)):
        if features[i] != 0 and imp > 0.01:
            display_name = SYMPTOM_DISPLAY_NAMES.get(col, col.replace("_", " ").title())
            feature_contributions.append({
                "feature": display_name,
                "importance": round(imp * 100, 2),
                "value": features[i]
            })

    # Sort by importance
    feature_contributions.sort(key=lambda x: x["importance"], reverse=True)
    top_factors = feature_contributions[:8]

    # Vital analysis
    vital_analysis = []
    vital_keys = ["heart_rate", "systolic_bp", "diastolic_bp", "temperature", "spo2", "bmi"]
    vital_names = ["Heart Rate", "Systolic BP", "Diastolic BP", "Temperature", "SpO2", "BMI"]

    for key, name in zip(vital_keys, vital_names):
        value = vitals.get(key, None)
        if value is not None:
            ranges = VITAL_RANGES[key]
            if ranges["normal"][0] <= value <= ranges["normal"][1]:
                status = "normal"
            elif ranges["warning"][0] <= value <= ranges["warning"][1]:
                status = "warning"
            else:
                status = "critical"
            vital_analysis.append({
                "name": name,
                "value": value,
                "status": status,
                "normal_range": f"{ranges['normal'][0]} - {ranges['normal'][1]}"
            })

    # Risk score calculation
    risk_score = round(risk_proba[2] * 100, 1) if len(risk_proba) > 2 else round(risk_proba[-1] * 100, 1)

    result = {
        "risk_level": risk_labels[risk_pred],
        "risk_score": risk_score,
        "risk_confidence": round(max(risk_proba) * 100, 1),
        "risk_probabilities": {
            label: round(prob * 100, 1)
            for label, prob in zip(risk_labels, risk_proba)
        },
        "triage": triage_labels[triage_pred],
        "triage_confidence": round(max(triage_proba) * 100, 1),
        "triage_probabilities": {
            label: round(prob * 100, 1)
            for label, prob in zip(triage_labels, triage_proba)
        },
        "top_contributing_factors": top_factors,
        "vital_analysis": vital_analysis,
        "recommendation": get_recommendation(risk_labels[risk_pred], triage_labels[triage_pred])
    }

    return result


def get_recommendation(risk_level, triage):
    """Get health recommendation based on risk level and triage."""
    recommendations = {
        ("High", "Emergency"): {
            "action": "Seek immediate medical attention",
            "description": "Your health indicators suggest a potentially serious condition. Please visit the nearest emergency room or call emergency services immediately.",
            "icon": "🚨",
            "color": "danger"
        },
        ("High", "Urgent"): {
            "action": "Visit a doctor within 24 hours",
            "description": "Your symptoms and vitals indicate elevated health risks. Schedule an urgent appointment with a healthcare provider as soon as possible.",
            "icon": "⚠️",
            "color": "warning"
        },
        ("Medium", "Emergency"): {
            "action": "Seek medical attention promptly",
            "description": "Some of your health indicators require medical evaluation. Visit a healthcare facility at your earliest convenience.",
            "icon": "⚠️",
            "color": "warning"
        },
        ("Medium", "Urgent"): {
            "action": "Schedule a medical consultation",
            "description": "Your health status shows moderate risk factors. It is recommended to consult with a healthcare professional within the next few days.",
            "icon": "📋",
            "color": "warning"
        },
        ("Medium", "Routine"): {
            "action": "Monitor and follow up",
            "description": "Your health indicators are mostly within acceptable ranges with some areas to monitor. Consider scheduling a routine check-up.",
            "icon": "📋",
            "color": "info"
        },
        ("Low", "Routine"): {
            "action": "Maintain healthy habits",
            "description": "Your health indicators appear to be within normal ranges. Continue maintaining a healthy lifestyle with regular check-ups.",
            "icon": "✅",
            "color": "success"
        },
        ("Low", "Urgent"): {
            "action": "Routine check-up recommended",
            "description": "While your overall risk appears low, some indicators suggest a routine medical check-up would be beneficial.",
            "icon": "📋",
            "color": "info"
        },
        ("Low", "Emergency"): {
            "action": "Consult with a healthcare provider",
            "description": "Some indicators need attention. Please consult with a healthcare provider for a thorough evaluation.",
            "icon": "📋",
            "color": "info"
        },
        ("High", "Routine"): {
            "action": "Medical evaluation needed",
            "description": "Your risk level suggests the need for medical evaluation. Please see a healthcare provider soon.",
            "icon": "⚠️",
            "color": "warning"
        }
    }
    return recommendations.get((risk_level, triage), {
        "action": "Consult a healthcare provider",
        "description": "Based on the analysis, we recommend consulting a healthcare professional for further evaluation.",
        "icon": "📋",
        "color": "info"
    })


# ====== Disease Prediction Based on Symptoms ======

DISEASE_PROFILES = [
    {
        "disease": "Influenza (Flu)",
        "symptoms": ["fever", "cough", "body_ache", "fatigue", "sore_throat", "runny_nose", "headache"],
        "specialist": "General Physician",
        "severity": "Moderate",
        "description": "A viral respiratory illness causing fever, body aches, and respiratory symptoms."
    },
    {
        "disease": "Common Cold",
        "symptoms": ["cough", "sore_throat", "runny_nose", "headache", "fatigue"],
        "specialist": "General Physician",
        "severity": "Mild",
        "description": "A mild viral infection of the upper respiratory tract."
    },
    {
        "disease": "Pneumonia",
        "symptoms": ["fever", "cough", "shortness_of_breath", "chest_pain", "fatigue", "body_ache"],
        "specialist": "Pulmonologist",
        "severity": "Severe",
        "description": "An infection that inflames the air sacs in one or both lungs, potentially serious."
    },
    {
        "disease": "COVID-19",
        "symptoms": ["fever", "cough", "shortness_of_breath", "fatigue", "body_ache", "loss_of_appetite", "headache", "sore_throat"],
        "specialist": "General Physician",
        "severity": "Moderate to Severe",
        "description": "A respiratory illness caused by SARS-CoV-2 coronavirus."
    },
    {
        "disease": "Dengue Fever",
        "symptoms": ["fever", "headache", "body_ache", "joint_pain", "nausea", "skin_rash", "fatigue"],
        "specialist": "General Physician",
        "severity": "Severe",
        "description": "A mosquito-borne viral disease causing high fever and severe body pain."
    },
    {
        "disease": "Malaria",
        "symptoms": ["fever", "headache", "nausea", "vomiting", "fatigue", "body_ache", "dizziness"],
        "specialist": "General Physician",
        "severity": "Severe",
        "description": "A parasitic disease transmitted by mosquitoes causing recurrent fever."
    },
    {
        "disease": "Typhoid Fever",
        "symptoms": ["fever", "headache", "abdominal_pain", "loss_of_appetite", "fatigue", "diarrhea"],
        "specialist": "General Physician",
        "severity": "Moderate to Severe",
        "description": "A bacterial infection from contaminated food or water."
    },
    {
        "disease": "Gastroenteritis",
        "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal_pain", "fever", "loss_of_appetite"],
        "specialist": "Gastroenterologist",
        "severity": "Moderate",
        "description": "An intestinal infection causing diarrhea, cramps, nausea, and vomiting."
    },
    {
        "disease": "Diabetes Mellitus",
        "symptoms": ["frequent_urination", "excessive_thirst", "weight_loss", "fatigue", "blurred_vision"],
        "specialist": "Endocrinologist",
        "severity": "Chronic",
        "description": "A metabolic disorder characterized by high blood sugar levels over a prolonged period."
    },
    {
        "disease": "Hypertension (High BP)",
        "symptoms": ["headache", "dizziness", "blurred_vision", "chest_pain", "shortness_of_breath"],
        "specialist": "Cardiologist",
        "severity": "Chronic",
        "description": "A condition where blood pressure against artery walls is consistently too high."
    },
    {
        "disease": "Heart Disease / Cardiac Event",
        "symptoms": ["chest_pain", "shortness_of_breath", "rapid_heartbeat", "dizziness", "fatigue", "nausea", "numbness"],
        "specialist": "Cardiologist",
        "severity": "Critical",
        "description": "Conditions involving the heart including coronary artery disease and arrhythmias."
    },
    {
        "disease": "Asthma / COPD",
        "symptoms": ["shortness_of_breath", "cough", "chest_pain", "fatigue"],
        "specialist": "Pulmonologist",
        "severity": "Moderate",
        "description": "Chronic respiratory conditions causing airway inflammation and breathing difficulty."
    },
    {
        "disease": "Stroke / TIA",
        "symptoms": ["confusion", "numbness", "headache", "blurred_vision", "dizziness", "rapid_heartbeat"],
        "specialist": "Neurologist",
        "severity": "Critical",
        "description": "A medical emergency where blood supply to part of the brain is interrupted."
    },
    {
        "disease": "Migraine",
        "symptoms": ["headache", "nausea", "blurred_vision", "dizziness", "fatigue"],
        "specialist": "Neurologist",
        "severity": "Moderate",
        "description": "A neurological condition causing intense, debilitating headaches with sensory disturbances."
    },
    {
        "disease": "Urinary Tract Infection (UTI)",
        "symptoms": ["frequent_urination", "fever", "abdominal_pain", "fatigue"],
        "specialist": "Urologist",
        "severity": "Moderate",
        "description": "An infection in any part of the urinary system."
    },
    {
        "disease": "Rheumatoid Arthritis",
        "symptoms": ["joint_pain", "swelling", "fatigue", "body_ache", "numbness"],
        "specialist": "Rheumatologist",
        "severity": "Chronic",
        "description": "An autoimmune disorder causing chronic joint inflammation and pain."
    },
    {
        "disease": "Allergic Reaction / Dermatitis",
        "symptoms": ["skin_rash", "swelling", "shortness_of_breath", "nausea"],
        "specialist": "Dermatologist",
        "severity": "Mild to Moderate",
        "description": "An immune system response to a foreign substance causing skin or systemic symptoms."
    },
    {
        "disease": "Anemia",
        "symptoms": ["fatigue", "dizziness", "shortness_of_breath", "headache", "rapid_heartbeat", "loss_of_appetite"],
        "specialist": "Hematologist",
        "severity": "Moderate",
        "description": "A condition where you lack enough healthy red blood cells to carry adequate oxygen."
    },
    {
        "disease": "Thyroid Disorder",
        "symptoms": ["fatigue", "weight_loss", "rapid_heartbeat", "swelling", "body_ache"],
        "specialist": "Endocrinologist",
        "severity": "Chronic",
        "description": "Conditions affecting the thyroid gland, impacting metabolism and energy levels."
    },
    {
        "disease": "Kidney Disease / Nephritis",
        "symptoms": ["swelling", "frequent_urination", "fatigue", "nausea", "loss_of_appetite", "dizziness"],
        "specialist": "Nephrologist",
        "severity": "Severe",
        "description": "Conditions where kidneys are damaged and cannot filter blood effectively."
    }
]


def predict_diseases(symptoms):
    """
    Predict possible diseases based on selected symptoms.
    Returns a sorted list of disease matches with confidence scores.
    """
    if not symptoms:
        return []

    matches = []
    symptom_set = set(symptoms)

    for profile in DISEASE_PROFILES:
        profile_symptoms = set(profile["symptoms"])
        # Calculate overlap
        common = symptom_set & profile_symptoms
        if len(common) < 2:
            continue  # Need at least 2 matching symptoms

        # Confidence = weighted score based on coverage
        # How much of the patient's symptoms match this disease
        patient_coverage = len(common) / len(symptom_set) if symptom_set else 0
        # How much of the disease's symptoms are present
        disease_coverage = len(common) / len(profile_symptoms)
        # Weighted average with more weight on disease coverage
        confidence = round((patient_coverage * 0.4 + disease_coverage * 0.6) * 100, 1)

        if confidence >= 20:
            matches.append({
                "disease": profile["disease"],
                "confidence": min(confidence, 95),
                "specialist": profile["specialist"],
                "severity": profile["severity"],
                "description": profile["description"],
                "matching_symptoms": [SYMPTOM_DISPLAY_NAMES.get(s, s) for s in common],
                "matching_count": len(common),
                "total_disease_symptoms": len(profile_symptoms)
            })

    # Sort by confidence descending
    matches.sort(key=lambda x: x["confidence"], reverse=True)
    return matches[:5]  # Return top 5 matches


if __name__ == "__main__":
    train_models()
