import React from 'react';
import { render, screen } from '@testing-library/react';
import AvailableOrders from '../components/Courier/AvailableOrders';
import api from '../services/api';

jest.mock('../services/api');

test('renders available orders', async () => {
  api.get.mockResolvedValue({ data: [{ id: 1 }] });
  render(<AvailableOrders />);
  expect(await screen.findByText('1')).toBeInTheDocument();
});