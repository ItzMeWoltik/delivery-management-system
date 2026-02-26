import React from 'react';
import { render, screen } from '@testing-library/react';
import ActiveOrders from '../components/Courier/ActiveOrders';
import api from '../services/api';

jest.mock('../services/api');

test('renders active orders', async () => {
  api.get.mockResolvedValue({ data: [{ id: 1, status: 'accepted' }] });
  render(<ActiveOrders />);
  expect(await screen.findByText('1 - accepted')).toBeInTheDocument();
});