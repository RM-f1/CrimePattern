import React, { useState } from 'react';
import Navbar from './Components/Navbar';
import Map from './Components/Map';
import Sidebar from './Components/Sidebar';
import AlertBanner from './Components/AlertBanner';

function App() {
  // 1. HARDCODED DATA: This mimics what Rakhi will send you later
  const mockCrimePoints = [
    [28.6139, 77.2090, 0.9], // Central Delhi - High Intensity
    [28.6250, 77.2100, 0.5], 
    [28.6100, 77.2300, 0.7],
    [28.6300, 77.2200, 0.4]
  ];

  // 2. STATE: Controls the "look" of the UI
  const [isDanger, setIsDanger] = useState(false);
  const [riskScore, setRiskScore] = useState(0.42); // Start with a "Safe" score

  // 3. SIMULATION FUNCTION: To show the judges the Alert Banner
  const toggleSimulation = () => {
    setIsDanger(!isDanger);
    setRiskScore(isDanger ? 0.42 : 0.88); // Switch between safe and dangerous
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: 'sans-serif' }}>
      <Navbar />
      
      {/* The banner shows based on our 'isDanger' toggle */}
      <AlertBanner show={isDanger} riskScore={riskScore} />

      <div style={{ display: 'flex', flex: 1, position: 'relative' }}>
        <div style={{ flex: 1 }}>
          {/* Map centers on Delhi and shows our mock heatpoints */}
          <Map crimePoints={mockCrimePoints} userLocation={[28.6139, 77.2090]} />
        </div>

        <Sidebar 
          riskScore={riskScore} 
          safeRoute={isDanger ? "STAY CLEAR: Avoid lanes near Connaught Place. Use Main Metro Route." : "Current route is clear."} 
        />

        {/* FLOATING BUTTON: Use this to 'Simulate' the danger for the demo */}
        <button 
          onClick={toggleSimulation}
          style={{
            position: 'absolute', bottom: '20px', left: '20px', zIndex: 1000,
            padding: '10px 20px', backgroundColor: '#333', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer'
          }}
        >
          {isDanger ? "Reset to Safe" : "Simulate Entering Danger Zone"}
        </button>
      </div>
    </div>
  );
}

export default App;