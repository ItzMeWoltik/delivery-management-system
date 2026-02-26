import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Chat from '../components/Chat';

test('renders chat', () => {
  render(<Chat room="test" />);
  expect(screen.getByText('Send')).toBeInTheDocument();
});

test('sends message', () => {
  const { getByPlaceholderText, getByText } = render(<Chat room="test" />);
  fireEvent.change(getByPlaceholderText(''), { target: { value: 'Hello' } });  // Assume input has no placeholder, adjust if needed
  fireEvent.click(getByText('Send'));
});