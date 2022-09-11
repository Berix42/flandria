import '@testing-library/jest-dom';
import React from 'react';
import { render, screen } from '@testing-library/react';
import LandingPage from '../../../components/home/LandingPage';

it('renders LandingPage component', () => {
  render(<LandingPage />);
  expect(screen.getByText('Your Florensia Database')).toBeInTheDocument();
});
