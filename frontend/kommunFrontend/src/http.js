import axios from 'axios'; 
const API_BASE_URL = 'http://127.0.0.1:8000/'; 

export default axios.create({
  baseURL: API_BASE_URL,
  //timeout: 1000,
  //headers: {'X-Custom-Header': 'foobar'}
});