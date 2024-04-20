import axios from 'axios'; 
const API_BASE_URL = 'https://burly-agreement-production.up.railway.app/'; 

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true

});

export default api;
