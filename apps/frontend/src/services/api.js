import axios from 'axios';

// Set the API base URL
const API_URL = 'http://localhost:8000';

// Create an axios instance with common configuration
export const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});