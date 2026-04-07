import React from 'react';

const AlertBanner = ({ show, riskScore }) => {
  if (!show) return null;
  return (
    <div style={{ backgroundColor: '#ff4d4d', color: 'white', padding: '15px', textAlign: 'center', fontWeight: 'bold', position: 'fixed', top: '60px', width: '100%', zIndex: 1000, boxShadow: '0 4px 6px rgba(0,0,0,0.2)' }}>
      ⚠️ WARNING: Entering High-Risk Zone (Risk Score: {(riskScore * 100).toFixed(1)}%)
    </div>
  );
};

export default AlertBanner;