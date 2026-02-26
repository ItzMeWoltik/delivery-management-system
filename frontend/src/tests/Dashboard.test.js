import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../components/Admin/Dashboard';
import api from '../services/api';

jest.mock('../services/api');

test('renders dashboard', async () => {
  api.get.mockResolvedValue({ data: { live_deliveries: 5, revenue: 100, active_couriers: 10 } });
  render(<Dashboard />);
  expect(await screen.findByText('Live Deliveries: 5')).toBeInTheDocument();
});