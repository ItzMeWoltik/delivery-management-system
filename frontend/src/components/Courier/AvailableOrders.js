import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const AvailableOrders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get('/couriers/orders/available');
        setOrders(response.data);
      } catch (error) {
        alert('Failed to load orders');
      }
    };
    fetchOrders();
  }, []);

  const handleAccept = async (orderId) => {
    try {
      await api.post(`/couriers/orders/${orderId}/accept`);
      alert(translate('order_accepted'));
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <ul>
      {orders.map(order => (
        <li key={order.id}>
          {order.id}
          <button onClick={() => handleAccept(order.id)}>{translate('accept')}</button>
        </li>
      ))}
    </ul>
  );
};

export default AvailableOrders;