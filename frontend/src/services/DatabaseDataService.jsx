import Axios from 'axios';
import { apiUrl } from '../constants';

function getDetailedData(tablename, code) {
  return Axios.get(`${apiUrl}/database/${tablename}/${code}`);
}

function getFilteredData(tablename, searchParams) {
  return Axios.get(`${apiUrl}/database/${tablename}?${searchParams}`);
}

function searchData(searchString) {
  return Axios.get(`${apiUrl}/database/search?s=${searchString}`);
}

function getMapData(mapCode) {
  return Axios.get(`${apiUrl}/database/map/${mapCode}`);
}

export {
  getDetailedData,
  getFilteredData,
  searchData,
  getMapData,
};
