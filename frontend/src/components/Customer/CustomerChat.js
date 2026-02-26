import React from 'react';
import Chat from '../Chat';

const CustomerChat = ({ orderId }) => {
  return <Chat room={`customer_courier_${orderId}`} />;
};

export default CustomerChat;