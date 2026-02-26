import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const OrderHistory = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get('/couriers/orders/history');
        setOrders(response.data);
      } catch (error) {
        alert('Failed to load history');
      }
    };
    fetchHistory();
  }, []);

  return (
    <ul>
      {orders.map(order => (
        <li key={order.id}>{`${order.id}: ${order.status}`}</li>
      ))}
    </ul>
  );
};

export default OrderHistory;