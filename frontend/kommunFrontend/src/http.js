import axios from 'axios'; 
import { getCookie } from '/src/utils/cookies.js';
const API_BASE_URL = 'http://127.0.0.1:8000/'; 

export default axios.create({
  baseURL: API_BASE_URL,
  //timeout: 1000,
  headers: {
    'X-CSRF-Token': getCookie('csrftoken'),
  }
});