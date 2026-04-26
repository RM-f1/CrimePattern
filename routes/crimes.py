from flask import Blueprint, jsonify, request
import pandas as pd
import os

crimes_bp = Blueprint("crimes", __name__)
# Robust path to find the CSV relative to this file
CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/crimes_clean.csv")

def load_crimes():
    df = pd.read_csv(CSV_PATH)
    df = df.rename(columns={"district": "name", "total_crimes": "total"})
    crime_cols = ["murder", "rape", "kidnapping", "robbery", "theft", "riots", "dowry_deaths"]
    # Finds the most common crime type for that area
    df["type"] = df[crime_cols].idxmax(axis=1).str.capitalize()
    return df

@crimes_bp.route("/crimes", methods=["GET"])
def get_crimes():
    if not os.path.exists(CSV_PATH):
        return jsonify({"error": "File not found"}), 500
    try:
        df = load_crimes()
        # Clean the data: remove rows where district is 'Total'
        df = df[df["name"].str.lower() != "total"]
        
        output_cols = ["name", "state", "lat", "lng", "type", "risk", "total", 
                       "murder", "rape", "kidnapping", "robbery", "theft", "riots", "dowry_deaths"]
        
        crimes = df[output_cols].to_dict(orient="records")
        return jsonify({
            "count": len(crimes),
            "crimes": crimes # React will look inside this key
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@crimes_bp.route("/crimes/states", methods=["GET"])
def get_states():
    if not os.path.exists(CSV_PATH): return jsonify({"error": "File not found"}), 500
    df = pd.read_csv(CSV_PATH)
    states = sorted(df["state"].unique().tolist())
    return jsonify({"states": states}), 200 # Fixed the 20000 typo