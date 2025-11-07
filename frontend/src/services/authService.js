// Archivo creado automáticamente
import api from './api'

export const authService = {
  async login(credentials) {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData)
    return response.data
  },

  async getProfile() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async updateProfile(userData) {
    const response = await api.put('/auth/update-profile', userData)
    return response.data
  },

  logout() {
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
  }
}