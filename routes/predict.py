from flask import Blueprint, request, jsonify
import os
import joblib
import pandas as pd

predict_bp = Blueprint("predict", __name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/crime_model.pkl")

                       # Load model
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully")
        print("Model expects features:", list(model.feature_names_in_))
    except Exception as e:
        print(f"Model failed to load: {e}")
else:
     print(f"Model not found at path: {MODEL_PATH} — using dummy risk score")

@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    lat = data.get("lat")
    lng = data.get("lng")

    if lat is None or lng is None:
        return jsonify({"error": "lat and lng are required fields"}), 400

    # Real  prediction
    if model:
        try:
            features = pd.DataFrame([{
                "murder": float(data.get("murder", 0)),
                "rape": float(data.get("rape", 0)),
                "kidnapping": float(data.get("kidnapping", 0)),
                "robbery": float(data.get("robbery", 0)),
                "theft": float(data.get("theft", 0)),
                "riots": float(data.get("riots", 0)),
                "dowry_deaths": float(data.get("dowry_deaths", 0)),
                "lat": float(lat),
                "lng": float(lng),
            }])
            proba = model.predict_proba(features)[0]
            risk_score = float(proba[1])
            confidence = float(max(proba))
            label = get_risk_label(risk_score)

            return jsonify({
                "risk": round(risk_score, 2),
                "confidence": round(confidence, 2),
                "label": label,
                "source": "model"
            }), 200

        except Exception as e:
            print(f"Model prediction error: {e} — falling back to dummy")

    # Dummy fallback
    dummy_risk = 0.82
    return jsonify({
        "risk": dummy_risk,
        "confidence": 0.91,
        "label": get_risk_label(dummy_risk),
        "source": "dummy"
    }), 200


def get_risk_label(score: float) -> str:
    if score >= 0.75:
        return "High Risk"
    elif score >= 0.45:
        return "Medium Risk"
    else:
        return "Low Risk"