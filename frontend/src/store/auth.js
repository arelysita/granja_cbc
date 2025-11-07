// Archivo creado automáticamente
import { defineStore } from 'pinia'
import { authService } from '../services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('authToken') || null,
    isLoading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.rol === 'administrador',
    isClient: (state) => state.user?.rol === 'cliente',
    userName: (state) => state.user?.nombre || state.user?.email
  },

  actions: {
    async login(credentials) {
      this.isLoading = true
      this.error = null
      
      try {
        const data = await authService.login(credentials)
        this.user = data.user
        this.token = data.access_token
        
        localStorage.setItem('authToken', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        return data
      } catch (error) {
        this.error = error.response?.data?.error || 'Error en el login'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async register(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        const data = await authService.register(userData)
        this.user = data.user
        this.token = data.access_token
        
        localStorage.setItem('authToken', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        return data
      } catch (error) {
        this.error = error.response?.data?.error || 'Error en el registro'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateProfile(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        const data = await authService.updateProfile(userData)
        this.user = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
        return data
      } catch (error) {
        this.error = error.response?.data?.error || 'Error actualizando perfil'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async checkAuth() {
      if (!this.token) return false
      
      try {
        const data = await authService.getProfile()
        this.user = data.user
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    logout() {
      authService.logout()
      this.user = null
      this.token = null
      this.error = null
      localStorage.removeItem('authToken')
      localStorage.removeItem('user')
    }
  }
})