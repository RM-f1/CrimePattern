import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Navbar from './Components/Navbar';
import Map from './Components/Map';
import Sidebar from './Components/Sidebar';
import AlertBanner from './Components/AlertBanner';

// THIS IS YOUR LIVE RENDER BACKEND URL
const API_URL = "https://crimepattern-backend.onrender.com";

function App() {
  const [crimePoints, setCrimePoints] = useState([]);
  const [riskScore, setRiskScore] = useState(0);
  
  // Default to Ludhiana coordinates [Lat, Lng]
  const [userLocation, setUserLocation] = useState([30.9010, 75.8573]);

  // --- 1. PREDICTION LOGIC (THE "PROBE") ---
  const predictRisk = useCallback(async (coords) => {
    try {
      const res = await axios.post(`${API_URL}/predict`, {
        lat: coords[0], 
        lng: coords[1],
        // Feeding these as defaults; your backend logic uses these if not in a red area
        murder: 1, theft: 50, robbery: 5 
      });
      setRiskScore(res.data.risk);
    } catch (err) {
      console.error("Prediction Error:", err);
    }
  }, []);

  // --- 2. INITIAL FETCH: LOAD THE HEATMAP ---
  useEffect(() => {
    const fetchCrimes = async () => {
      try {
        const res = await axios.get(`${API_URL}/crimes`);
        // Assuming your backend returns { crimes: [{lat, lng}, ...] }
        const formatted = res.data.crimes.map(c => [c.lat, c.lng, 1.0]);
        setCrimePoints(formatted);
      } catch (err) {
        console.error("Error fetching crime data:", err);
      }
    };
    fetchCrimes();
  }, []);

  // --- 3. GPS TRACKING (MOVES THE BLUE PIN) ---
  useEffect(() => {
    if (navigator.geolocation) {
      const watchId = navigator.geolocation.watchPosition((pos) => {
        const coords = [pos.coords.latitude, pos.coords.longitude];
        setUserLocation(coords); // Update marker position
        predictRisk(coords);     // Update risk for current location
      }, (err) => console.warn("GPS Error:", err), { enableHighAccuracy: true });

      return () => navigator.geolocation.clearWatch(watchId);
    }
  }, [predictRisk]);

  // --- 4. MAP CLICK LOGIC (SCANNER MODE) ---
  const handleMapClick = (clickedCoords) => {
    // Only call the API to get the risk for that spot.
    // The Blue Pin (userLocation) stays exactly where it is!
    predictRisk(clickedCoords);
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: '#0a1628' }}>
      <Navbar />
      
      {/* Banner pops up automatically if risk > 70% */}
      <AlertBanner show={riskScore > 0.7} riskScore={riskScore} />

      <div style={{ display: 'flex', flex: 1, position: 'relative' }}>
        <div style={{ flex: 1 }}>
          <Map 
            crimePoints={crimePoints} 
            userLocation={userLocation} 
            onMapClick={handleMapClick} 
          />
        </div>

        <Sidebar 
          riskScore={riskScore} 
          safeRoute={riskScore > 0.7 
            ? "🚨 DANGER: High risk zone detected! Seek well-lit main roads." 
            : "✅ Safe Zone: Area is currently stable."
          } 
        />
      </div>
    </div>
  );
}

export default App;