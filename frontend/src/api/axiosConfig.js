import axios from 'axios';

// 🔥 CONFIGURAR LA URL BASE CORRECTA para tu backend Flask
const API_BASE_URL = 'http://localhost:5000'; // Puerto por defecto de Flask

axios.defaults.baseURL = API_BASE_URL;

// Interceptor para agregar token automáticamente
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    config.headers['Content-Type'] = 'application/json';
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de autenticación
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 422) {
      console.log('Token inválido - Limpiando datos y redirigiendo');
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default axios;