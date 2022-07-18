import React from 'react';
import { Navigate, useLocation, Outlet } from 'react-router-dom';
import { isAuthenticated } from './components/auth/auth';

const ProtectedRoutes = () => {
  const location = useLocation();
  // Pass previous state
  const newState = location.state ?? {};
  // Pass current- as redirect-location
  newState.from = location;

  return isAuthenticated() ? (
    <Outlet />
  ) : (
    <Navigate to="/auth/login" replace state={newState} />
  );
};

export default ProtectedRoutes;
