import React, { useState } from 'react';
import api from '../../services/api';
import { translate } from '../../utils/i18n';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('customer');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/auth/register', { email, password, role });
      alert('Registered');
    } catch (error) {
      alert('Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder={translate('email')} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder={translate('password')} />
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="customer">{translate('customer')}</option>
        <option value="courier">{translate('courier')}</option>
      </select>
      <button type="submit">{translate('register')}</button>
    </form>
  );
};

export default Register;