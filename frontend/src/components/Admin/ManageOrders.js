import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const ManageOrders = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await api.get('/admin/orders');
        setOrders(response.data);
      } catch (error) {
        alert('Failed to load orders');
      }
    };
    fetchOrders();
  }, []);

  const handleForceCancel = async (orderId) => {
    try {
      await api.post(`/admin/orders/${orderId}/force_cancel`);
      alert(translate('order_force_cancelled'));
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <ul>
      {orders.map(order => (
        <li key={order.id}>
          {order.id} - {order.status}
          <button onClick={() => handleForceCancel(order.id)}>{translate('force_cancel')}</button>
        </li>
      ))}
    </ul>
  );
};

export default ManageOrders;