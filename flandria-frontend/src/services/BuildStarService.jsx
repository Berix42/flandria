import Axios from 'axios';
import { apiUrl } from '../constants';
import { getToken } from './AuthService';

function addStar(buildId) {
  return Axios.post(
    `${apiUrl}/planner/builds/${buildId}/star/add`,
    {},
    { headers: { Authorization: `Bearer ${getToken()}` } },
  );
}

function deleteStar(buildId) {
  return Axios.delete(
    `${apiUrl}/planner/builds/${buildId}/star/delete`,
    { headers: { Authorization: `Bearer ${getToken()}` } },
  );
}

export {
  addStar,
  deleteStar,
};
