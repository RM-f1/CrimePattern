from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)                              

from routes.crimes import crimes_bp
from routes.predict import predict_bp

app.register_blueprint(crimes_bp)
app.register_blueprint(predict_bp)

@app.route("/", methods=["GET"])
def health_check():
    return {"status": "CrimePattern API is running"}, 200

if __name__ == "__main__":
    app.run(debug=True)