import React, { useEffect } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat';
import L from 'leaflet';

const HeatmapLayer = ({ points }) => {
  const map = useMap();
  useEffect(() => {
    if (points.length > 0) {
      // Points format: [[lat, lng, intensity], ...]
      const heat = L.heatLayer(points, { radius: 25, blur: 15, maxZoom: 17 }).addTo(map);
      return () => map.removeLayer(heat);
    }
  }, [map, points]);
  return null;
};

const Map = ({ crimePoints, userLocation }) => {
  return (
    <MapContainer center={userLocation} zoom={13} style={{ height: '100%', width: '100%' }}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <HeatmapLayer points={crimePoints} />
    </MapContainer>
  );
};

export default Map;