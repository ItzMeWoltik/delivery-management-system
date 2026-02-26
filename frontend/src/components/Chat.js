import React, { useEffect, useState } from 'react';

const Chat = ({ room }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket(`ws://localhost:8000/ws/chat/${room}`);
    websocket.onopen = () => console.log('Connected');
    websocket.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };
    setWs(websocket);

    return () => websocket.close();
  }, [room]);

  const sendMessage = () => {
    if (ws) {
      ws.send(message);
      setMessage('');
    }
  };

  return (
    <div>
      <ul>
        {messages.map((msg, index) => <li key={index}>{msg}</li>)}
      </ul>
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default Chat;