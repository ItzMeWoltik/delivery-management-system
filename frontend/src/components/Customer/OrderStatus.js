import React, { useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const OrderStatus = () => {
  const [orderId, setOrderId] = useState('');
  const [status, setStatus] = useState('');

  const handleCheck = async () => {
    try {
      const response = await api.get(`/customers/orders/${orderId}/status`);
      setStatus(response.data.status);
    } catch (error) {
      alert('Failed to get status');
    }
  };

  return (
    <div>
      <input value={orderId} onChange={(e) => setOrderId(e.target.value)} placeholder={translate('order_id')} />
      <button onClick={handleCheck}>{translate('check_status')}</button>
      <p>{status ? `${translate('status')}: ${status}` : ''}</p>
    </div>
  );
};

export default OrderStatus;