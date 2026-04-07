import React from 'react';

const Sidebar = ({ riskScore, safeRoute }) => (
  <div style={{ width: '300px', padding: '20px', backgroundColor: '#f4f4f4', borderLeft: '2px solid #ddd', height: 'calc(100vh - 60px)', overflowY: 'auto' }}>
    <h3>Risk Analysis</h3>
    <div style={{ fontSize: '2rem', color: riskScore > 0.7 ? 'red' : 'green', margin: '20px 0' }}>
      {(riskScore * 100).toFixed(0)}%
    </div>
    <p><strong>Predicted Risk:</strong> {riskScore > 0.7 ? "High" : "Low"}</p>
    <hr />
    <h4>🛡️ Safe Route Suggestion</h4>
    <p>{safeRoute || "Analyzing current surroundings..."}</p>
  </div>
);

export default Sidebar;