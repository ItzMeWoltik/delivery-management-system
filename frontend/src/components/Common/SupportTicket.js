import React, { useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const SupportTicket = () => {
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/chats/tickets', { description });
      alert(`Ticket ID: ${response.data.ticket_id}`);
    } catch (error) {
      alert('Failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea value={description} onChange={(e) => setDescription(e.target.value)} placeholder={translate('description')} />
      <button type="submit">{translate('create_ticket')}</button>
    </form>
  );
};

export default SupportTicket;