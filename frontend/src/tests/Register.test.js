import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Register from '../components/Auth/Register';
import api from '../services/api';

jest.mock('../services/api');

test('renders register form', () => {
  render(<Register />);
  expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
});

test('submits form', async () => {
  api.post.mockResolvedValue({});
  render(<Register />);
  fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'pass' } });
  fireEvent.click(screen.getByText('Register'));
  expect(api.post).toHaveBeenCalledWith('/auth/register', { email: 'test@example.com', password: 'pass', role: 'customer' });
});