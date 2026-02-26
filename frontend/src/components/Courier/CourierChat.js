import React from 'react';
import Chat from '../Chat';

const CourierChat = ({ orderId }) => {
  return <Chat room={`customer_courier_${orderId}`} />;
};

export default CourierChat;