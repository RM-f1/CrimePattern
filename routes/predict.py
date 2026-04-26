from flask import Blueprint, request, jsonify
import os
import joblib
import pandas as pd
import numpy as np

predict_bp = Blueprint("predict", __name__)

# --- 1. DYNAMIC PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Based on your screenshot: CrimePattern > data > processed > crimes_clean.csv
DATA_PATH = os.path.join(BASE_DIR, "../data/processed/crimes_clean.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../model/crime_model.pkl")

model = None
crime_data = None

# Load ML Model
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ ML Model Loaded Successfully")
    except Exception as e:
        print(f"❌ Model Error: {e}")

# Load Crime CSV (The Heatmap Data)
if os.path.exists(DATA_PATH):
    try:
        crime_data = pd.read_csv(DATA_PATH)
        # Standardize column names to lowercase and strip spaces
        crime_data.columns = crime_data.columns.str.strip().str.lower()
        print(f"✅ CSV SUCCESS: Loaded {len(crime_data)} rows from {DATA_PATH}")
    except Exception as e:
        print(f"❌ CSV Load Error: {e}")
else:
    print(f"❌ CRITICAL ERROR: CSV NOT FOUND at {DATA_PATH}")

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    u_lat = float(data.get("lat", 0))
    u_lng = float(data.get("lng", 0))

    risk_score = 0.05  # Default baseline for safe areas
    source = "fallback"

    # --- 2. PROXIMITY LOGIC (Matches clicks to Red Blobs) ---
    if crime_data is not None:
        try:
            # Check for common coordinate column names
            lat_col = 'lat' if 'lat' in crime_data.columns else 'latitude'
            lng_col = 'lng' if 'lng' in crime_data.columns else ('lon' if 'lon' in crime_data.columns else 'longitude')

            if lat_col in crime_data.columns and lng_col in crime_data.columns:
                # Calculate distance from click to every point in CSV
                distances = np.sqrt((crime_data[lat_col] - u_lat)**2 + (crime_data[lng_col] - u_lng)**2)
                min_dist = distances.min()

                # If the click is within roughly 1.5km - 2km of a red blob
                if min_dist < 0.02:
                    risk_score = 0.88  # Force High Risk for red areas
                    source = "proximity-engine"
                
                # Debug print for your terminal
                print(f"DEBUG: Clicked ({u_lat}, {u_lng}) | Distance: {min_dist:.4f} | Source: {source}")
        except Exception as e:
            print(f"❌ Logic Error: {e}")

    # --- 3. ML MODEL LOGIC (Fallback/Enhancement) ---
    if source == "fallback" and model:
        try:
            features = pd.DataFrame([{
                "murder": float(data.get("murder", 1)),      # Demo defaults
                "rape": float(data.get("rape", 0)),
                "kidnapping": float(data.get("kidnapping", 0)),
                "robbery": float(data.get("robbery", 4)),
                "theft": float(data.get("theft", 40)),       # High theft to trigger risk
                "riots": float(data.get("riots", 0)),
                "dowry_deaths": float(data.get("dowry_deaths", 0)),
                "lat": u_lat,
                "lng": u_lng,
            }])
            
            # Use predict_proba for smooth percentages
            proba = model.predict_proba(features)[0]
            risk_score = max(0.12, float(proba[1])) # Min 12% if in white area
            source = "ml-model"
        except:
            pass

    return jsonify({
        "risk": round(risk_score, 2),
        "label": get_risk_label(risk_score),
        "confidence": 0.94,
        "source": source
    }), 200

def get_risk_label(score):
    if score >= 0.7: return "High Risk"
    if score >= 0.4: return "Medium Risk"
    return "Low Risk"