import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logoutUser } from './auth';

const LogoutView = () => {
  const navigate = useNavigate();

  useEffect(() => {
    logoutUser();
    navigate('/');
  }, []);

  return null;
};

export default LogoutView;
