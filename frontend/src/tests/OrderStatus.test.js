import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import OrderStatus from '../components/Customer/OrderStatus';
import api from '../services/api';

jest.mock('../services/api');

test('renders order status checker', () => {
  render(<OrderStatus />);
  expect(screen.getByPlaceholderText('Order ID')).toBeInTheDocument();
});

test('checks status', async () => {
  api.get.mockResolvedValue({ data: { status: 'pending' } });
  render(<OrderStatus />);
  fireEvent.change(screen.getByPlaceholderText('Order ID'), { target: { value: '1' } });
  fireEvent.click(screen.getByText('Check Status'));
  expect(api.get).toHaveBeenCalledWith('/customers/orders/1/status');
});