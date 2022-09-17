import Axios from 'axios';
import { apiUrl } from '../constants';
import { getToken } from './AuthService';

function getPlanner(classname) {
  return Axios.get(`${apiUrl}/planner/${classname}`);
}

function getBuilds(classname) {
  return Axios.get(`${apiUrl}/planner/builds/${classname}`);
}

function addBuild(title, description, hash, characterClass) {
  return Axios.post(
    `${apiUrl}/planner/builds`,
    {
      // Backend checks field-names
      title, description, hash, character_class: characterClass,
    },
    { headers: { Authorization: `Bearer ${getToken()}` } },
  );
}

function deleteBuild(buildId) {
  return Axios.delete(
    `${apiUrl}/planner/builds/${buildId}`,
    { headers: { Authorization: `Bearer ${getToken()}` } },
  );
}

export {
  getPlanner,
  getBuilds,
  addBuild,
  deleteBuild,
};
