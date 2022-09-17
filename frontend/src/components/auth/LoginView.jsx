import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { setWindowTitle } from '../../helpers';
import AuthWrapper from './AuthWrapper';
import { login, loginUser } from '../../services/AuthService';

const LoginView = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fieldErrors, setFieldErrors] = useState([]);

  useEffect(() => {
    setWindowTitle('Sign In');
  }, []);

  const onSubmit = async (event) => {
    setFieldErrors([]);
    event.preventDefault();

    // Check if all fields have some text in it
    const fields = [username, password];
    let fieldsValid = true;
    fields.forEach((field) => {
      if (field.length === 0) {
        fieldsValid = false;
      }
    });
    if (!fieldsValid) {
      setFieldErrors(['Please fill out all fields.']);
      return null;
    }

    // Request a JWT token
    // Redirect to the home page on success
    try {
      const resp = await login(username, password);
      loginUser(resp.data.access_token);
      // Redirect back to origin page with state
      navigate(location.state?.from ?? '/', { replace: true, state: location.state });
    } catch (error) {
      const errorMessage = error.response.data.message;
      setFieldErrors([errorMessage]);
    }

    return null;
  };

  return (
    <AuthWrapper>
      <h2 className="text-2xl font-bold text-slate-900 md:text-5xl dark:text-white">Sign In</h2>
      <form className="flex flex-col w-full gap-4" onSubmit={onSubmit}>
        <input
          className="text-input"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="text-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <div className="flex flex-col h-12 gap-2 overflow-auto text-red-400 dark:text-red-600 max-h-12">
          {fieldErrors.map((error) => <span key={error}>{error}</span>)}
        </div>
        <p className="flex justify-center whitespace-pre-wrap text-sm text-slate-900 dark:text-white">
          Do not have an account yet? Sign up
          {' '}
          <Link
            to="/auth/register"
            state={location.state}
            className="text-blue-500 dark:text-blue-600"
          >
            here
          </Link>
        </p>
        <div className="flex justify-center">
          <button type="submit" className="px-16 py-2 text-xl font-semibold tracking-wider text-white uppercase bg-emerald-400 rounded-full outline-none dark:bg-emerald-600 focus-within:outline-none hover:bg-emerald-500 dark:hover:bg-emerald-500">
            Sign In
          </button>
        </div>
      </form>
    </AuthWrapper>
  );
};

export default LoginView;
