# 🩸 CrimePattern

### **CrimePattern by PixelPulse**
> **Making cities safer, one prediction at a time.**

---

## 🌑 Overview
**CrimePattern** is a high-performance urban safety application. [cite: 130] [cite_start]By synthesizing historical data with machine learning, we identify high-risk zones and provide real-time alerts to ensure users stay informed of their surroundings.

## 🏗️ The Bloodline (Architecture)
The system is divided into three specialized nodes: 

***Data & ML (Ramandeep):** Cleans raw NCRB data and trains a **Random Forest** model to predict crime risks. 
* **Backend (Rakhi):** A **Flask API** that serves the intelligence layer and manages data routes. 
***Frontend (Navneet):** A **React** interface utilizing **Leaflet** for immersive heatmap visualizations. 

---

## 💉 Connectivity Flow
The data pulse moves through the following pipeline:
`Ramandeep (Data)` → `crimes_clean.csv + crime_model.pkl` → `Rakhi (Backend)` → `/predict & /crimes` → `Navneet (Frontend)` → `Heatmap + Alerts`

---

## 📂 Vault Structure
> **Note:** All project files are consolidated in the **Main Branch** for seamless evaluation.

### 🗡️ Backend & Intelligence
* `backend/data/` — Contains raw and processed NCRB datasets covering **688 districts**.
* `backend/model/` — Includes `train_model.py` and the saved `crime_model.pkl` with **89.13% accuracy**.
  `backend/app.py` — The primary heartbeat of the Flask API. 

### 👁️ Frontend & Visualization
* +`frontend/src/components/Map.jsx` — The core Leaflet heatmap layer. 
* `frontend/src/components/AlertBanner.jsx` — Visual triggers for high-risk zones based on model thresholds.

---

