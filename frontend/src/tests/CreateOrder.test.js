import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CreateOrder from '../components/Customer/CreateOrder';
import api from '../services/api';

jest.mock('../services/api');

test('renders create order form', () => {
  render(<CreateOrder />);
  expect(screen.getByPlaceholderText('From Address')).toBeInTheDocument();
});

test('submits order', async () => {
  api.post.mockResolvedValue({ data: { order_id: 1 } });
  render(<CreateOrder />);
  fireEvent.change(screen.getByPlaceholderText('From Address'), { target: { value: 'From' } });
  fireEvent.change(screen.getByPlaceholderText('To Address'), { target: { value: 'To' } });
  fireEvent.click(screen.getByText('Create Order'));
  expect(api.post).toHaveBeenCalledWith('/customers/orders', { from_address: 'From', to_address: 'To' });
});