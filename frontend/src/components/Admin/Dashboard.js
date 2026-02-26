import React, { useEffect, useState } from 'react';
import api from '../../services/api';

const Dashboard = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/admin/dashboard');
        setData(response.data);
      } catch (error) {
        alert('Failed to load dashboard');
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <p>Live Deliveries: {data.live_deliveries}</p>
      <p>Revenue: {data.revenue}</p>
      <p>Active Couriers: {data.active_couriers}</p>
    </div>
  );
};

export default Dashboard;