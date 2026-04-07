from flask import Blueprint, jsonify, request
import pandas as pd
import os

crimes_bp = Blueprint("crimes", __name__)
CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/crimes_clean.csv")


def load_crimes():
    """Load and prepare crimes dataframe from CSV."""
    df = pd.read_csv(CSV_PATH)

    df = df.rename(columns={
        "district": "name",
        "total_crimes": "total"
    })

    crime_cols = ["murder", "rape", "kidnapping", "robbery", "theft", "riots", "dowry_deaths"]
    df["type"] = df[crime_cols].idxmax(axis=1).str.capitalize()

    return df


@crimes_bp.route("/crimes", methods=["GET"])
def get_crimes():
    if not os.path.exists(CSV_PATH):
        return jsonify({"error": f"crimes_clean.csv not found at {CSV_PATH}"}), 500

    try:
        df = load_crimes()

        state_filter = request.args.get("state")
        risk_filter = request.args.get("risk")

        if state_filter:
            df = df[df["state"].str.lower() == state_filter.lower()]

        if risk_filter is not None:
            df = df[df["risk"] == int(risk_filter)]

        df = df[df["name"].str.lower() != "total"]
        output_cols = ["name", "state", "lat", "lng", "type", "risk",
                       "total", "murder", "rape", "kidnapping",
                       "robbery", "theft", "riots", "dowry_deaths"]

        crimes = df[output_cols].to_dict(orient="records")

        return jsonify({
            "count": len(crimes),
            "crimes": crimes
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crimes_bp.route("/crimes/states", methods=["GET"])
def get_states():
    if not os.path.exists(CSV_PATH):
        return jsonify({
            "error": "crimes_clean.csv not found"
        }), 500

    df = pd.read_csv(CSV_PATH)
    states = sorted(df["state"].unique().tolist())
    return jsonify({"states": states}), 20000