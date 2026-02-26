import React, { useEffect, useState } from 'react';
import api from '../../services/api';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await api.get('/admin/alerts');
        setAlerts(response.data);
      } catch (error) {
        alert('Failed to load alerts');
      }
    };
    fetchAlerts();
  }, []);

  return (
    <ul>
      {alerts.map((al, index) => (
        <li key={index}>{al.type} - {al.date}</li>
      ))}
    </ul>
  );
};

export default Alerts;