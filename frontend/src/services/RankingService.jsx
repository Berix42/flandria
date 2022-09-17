import Axios from 'axios';
import { apiUrl } from '../constants';

function getGuildsRanking(searchParams) {
  return Axios.get(`${apiUrl}/ranking/guilds?${searchParams}`);
}

function getGuildRanking(guildName) {
  return Axios.get(`${apiUrl}/ranking/guilds/${guildName}`);
}

function getPlayerRanking(server, playerName) {
  return Axios.get(`${apiUrl}/ranking/players/${server}/${playerName}`);
}

function getStatistics(searchParams) {
  return Axios.get(`${apiUrl}/ranking/statistics?${searchParams}`);
}

export {
  getGuildsRanking,
  getGuildRanking,
  getPlayerRanking,
  getStatistics,
};
