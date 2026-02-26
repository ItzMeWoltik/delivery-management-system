import React, { useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const LocationUpdate = () => {
  const [lat, setLat] = useState(0);
  const [lon, setLon] = useState(0);

  const handleUpdate = async () => {
    try {
      await api.post('/couriers/location/update', { lat, lon });
      alert(translate('location_updated'));
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <div>
      <input type="number" value={lat} onChange={(e) => setLat(parseFloat(e.target.value))} placeholder="Lat" />
      <input type="number" value={lon} onChange={(e) => setLon(parseFloat(e.target.value))} placeholder="Lon" />
      <button onClick={handleUpdate}>{translate('update_location')}</button>
    </div>
  );
};

export default LocationUpdate;