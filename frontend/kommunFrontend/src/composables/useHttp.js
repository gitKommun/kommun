import axios from 'axios'; 
import { getCookie } from '/src/utils/cookies.js';

const API_BASE_URL = 'http://127.0.0.1:8000/'; 

export function useHttp() { 
    return axios.create({
        baseURL: API_BASE_URL,
        withCredentials: true,
        headers: {
            'x-csrftoken': getCookie('csrftoken'),
        }
    });
}