import React, { useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const CreateOrder = () => {
  const [fromAddress, setFromAddress] = useState('');
  const [toAddress, setToAddress] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/customers/orders', { from_address: fromAddress, to_address: toAddress });
      alert(`${translate('order_created')} ID: ${response.data.order_id}`);
    } catch (error) {
      alert('Failed to create order');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={fromAddress} onChange={(e) => setFromAddress(e.target.value)} placeholder={translate('from_address')} />
      <input value={toAddress} onChange={(e) => setToAddress(e.target.value)} placeholder={translate('to_address')} />
      <button type="submit">{translate('create_order')}</button>
    </form>
  );
};

export default CreateOrder;