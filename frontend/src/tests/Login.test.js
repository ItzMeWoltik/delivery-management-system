import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { AuthContext } from '../contexts/AuthContext';
import Login from '../components/Auth/Login';
import api from '../services/api';

jest.mock('../services/api');

const mockLogin = jest.fn();

const renderLogin = () => render(
  <AuthContext.Provider value={{ login: mockLogin }}>
    <Login />
  </AuthContext.Provider>
);

test('renders login form', () => {
  renderLogin();
  expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
});

test('submits form', async () => {
  api.post.mockResolvedValue({ data: { access_token: 'token' } });
  renderLogin();
  fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'pass' } });
  fireEvent.click(screen.getByText('Login'));
  expect(api.post).toHaveBeenCalledWith('/auth/login', { email: 'test@example.com', password: 'pass' });
  expect(mockLogin).toHaveBeenCalledWith('token');
});