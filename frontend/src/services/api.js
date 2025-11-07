// api.js
import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para agregar token a las requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')

    // Definir rutas públicas solo para GET
    const publicEndpoints = [
      { url: '/products', method: 'get' },
      { url: '/categories', method: 'get' }
    ]

    const isPublic = publicEndpoints.some(
      e => config.url.includes(e.url) && config.method.toLowerCase() === e.method
    )

    if (token && !isPublic) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar respuestas
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
