import Axios from 'axios';
import decode from 'jwt-decode';
import { getApiUrl } from '../helpers';

const localStorageKey = 'ACCESS_TOKEN_FLANDRIA_V1.2';
const apiUrl = getApiUrl();

function login(username, password) {
  return Axios.post(`${apiUrl}/auth/login`, { username, password });
}

function register(username, password) {
  return Axios.post(`${apiUrl}/auth/register`, { username, password });
}

function getToken() {
  return localStorage.getItem(localStorageKey) || null;
}

function isAuthenticated() {
  // Returns true if a token is found, however,
  // the token does not have to be valid.
  return getToken() !== null;
}

function loginUser(token) {
  localStorage.setItem(localStorageKey, token);
  window.dispatchEvent(new Event('storage'));
}

function logoutUser() {
  localStorage.removeItem(localStorageKey);
  window.dispatchEvent(new Event('storage'));
}

function getIdentity() {
  return decode(getToken()).identity;
}

export {
  login,
  register,
  isAuthenticated,
  getIdentity,
  loginUser,
  logoutUser,
  getToken,
};
