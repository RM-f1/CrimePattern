import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Circle, useMap, useMapEvents } from 'react-leaflet';
import { HeatmapLayer } from 'react-leaflet-heatmap-layer-v3';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// RELIABLE ICON FIX: Using direct CDN links to ensure the pin appears
const customIcon = new L.Icon({
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

// Component to force Leaflet to recalculate its size
function MapResizer() {
  const map = useMap();
  useEffect(() => {
    setTimeout(() => {
      map.invalidateSize();
    }, 500); // Wait 500ms for CSS to settle
  }, [map]);
  return null;
}

function MapEvents({ onMapClick }) {
  useMapEvents({
    click: (e) => onMapClick([e.latlng.lat, e.latlng.lng]),
  });
  return null;
}

function Map({ crimePoints, userLocation, onMapClick }) {
  const [isReady, setIsReady] = useState(false);

  // Delay heatmap rendering to prevent the IndexSizeError
  useEffect(() => {
    const timer = setTimeout(() => setIsReady(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ height: '100%', width: '100%', position: 'relative' }}>
      <MapContainer 
        center={userLocation} 
        zoom={13} 
        style={{ height: '100%', width: '100%', background: '#1a1a1a' }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        
        <MapResizer />
        <MapEvents onMapClick={onMapClick} />

        {/* Only render heatmap once the container has a width > 0 */}
        {isReady && crimePoints.length > 0 && (
          <HeatmapLayer
            points={crimePoints}
            longitudeExtractor={m => m[1]}
            latitudeExtractor={m => m[0]}
            intensityExtractor={m => parseFloat(m[2])}
            max={1.0}
            radius={30}
            blur={20}
          />
        )}

        {/* Updated Marker with customIcon to fix visibility */}
        <Marker position={userLocation} icon={customIcon} />
        
        <Circle 
          center={userLocation} 
          radius={600} 
          pathOptions={{ color: '#1a73e8', fillColor: '#1a73e8', fillOpacity: 0.1 }} 
        />
      </MapContainer>
    </div>
  );
}

export default Map;