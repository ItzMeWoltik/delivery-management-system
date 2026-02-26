import React, { useState } from 'react';
import api from '../../services/api';

const GeoView = () => {
  const [courierId, setCourierId] = useState('');
  const [locations, setLocations] = useState([]);

  const handleView = async () => {
    try {
      const response = await api.get(`/geo/couriers/${courierId}/locations`);
      setLocations(response.data);
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <div>
      <input value={courierId} onChange={(e) => setCourierId(e.target.value)} placeholder="Courier ID" />
      <button onClick={handleView}>View Locations</button>
      <ul>
        {locations.map((loc, index) => <li key={index}>{`Lat: ${loc.lat}, Lon: ${loc.lon}`}</li>)}
      </ul>
    </div>
  );
};

export default GeoView;