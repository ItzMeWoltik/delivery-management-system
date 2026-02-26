import React from 'react';
import { render, screen } from '@testing-library/react';
import OrderHistory from '../components/Customer/OrderHistory';
import api from '../services/api';

jest.mock('../services/api');

test('renders order history', async () => {
  api.get.mockResolvedValue({ data: [{ id: 1, status: 'pending' }] });
  render(<OrderHistory />);
  expect(await screen.findByText('1: pending')).toBeInTheDocument();
});