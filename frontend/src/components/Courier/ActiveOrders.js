import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const ActiveOrders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get('/couriers/orders/active');
        setOrders(response.data);
      } catch (error) {
        alert('Failed to load orders');
      }
    };
    fetchOrders();
  }, []);

  const handleStart = async (orderId) => {
    try {
      await api.post(`/couriers/orders/${orderId}/start`);
      alert(translate('delivery_started'));
    } catch (error) {
      alert('Failed');
    }
  };

  const handleComplete = async (orderId) => {
    try {
      await api.post(`/couriers/orders/${orderId}/complete`);
      alert(translate('delivery_completed'));
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <ul>
      {orders.map(order => (
        <li key={order.id}>
          {order.id} - {order.status}
          <button onClick={() => handleStart(order.id)}>{translate('start')}</button>
          <button onClick={() => handleComplete(order.id)}>{translate('complete')}</button>
        </li>
      ))}
    </ul>
  );
};

export default ActiveOrders;