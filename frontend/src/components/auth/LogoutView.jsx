import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logoutUser } from '../../services/AuthService';

const LogoutView = () => {
  const navigate = useNavigate();

  useEffect(() => {
    logoutUser();
    navigate('/');
  }, []);

  return null;
};

export default LogoutView;
