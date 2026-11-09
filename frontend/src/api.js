// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // Благодаря прокси, запросы идут на Django
});

// Добавляем токен к каждому запросу
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;