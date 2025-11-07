import { defineStore } from 'pinia'

export const useOrdersStore = defineStore('orders', {
  state: () => ({
    orders: [],
    isLoading: false,
    error: null
  }),

  getters: {
    isEmpty: (state) => state.orders.length === 0,
    getOrderById: (state) => (orderId) => {
      return state.orders.find(order => order.id === orderId)
    },
    sortedOrders: (state) => {
      return [...state.orders].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }
  },

  actions: {
    // Crear nueva orden
    createOrder(orderData) {
      try {
        console.log('🔄 Creando nueva orden local...', orderData)
        
        const newOrder = {
          id: Date.now().toString(),
          order_number: 'ORD-' + Date.now().toString().slice(-8),
          ...orderData,
          created_at: new Date().toISOString(),
          status: 'completed'
        }
        
        this.orders.unshift(newOrder)
        this.saveToLocalStorage()
        
        console.log('✅ Orden creada localmente:', newOrder)
        return newOrder
        
      } catch (error) {
        console.error('❌ Error creando orden local:', error)
        this.error = error.message
        throw error
      }
    },

    // Cargar órdenes desde localStorage
    loadFromLocalStorage() {
      try {
        const savedOrders = localStorage.getItem('localOrders')
        if (savedOrders) {
          this.orders = JSON.parse(savedOrders)
          console.log('📦 Órdenes cargadas desde localStorage:', this.orders.length)
        } else {
          console.log('📭 No hay órdenes guardadas en localStorage')
          this.orders = []
        }
      } catch (error) {
        console.error('❌ Error cargando órdenes desde localStorage:', error)
        this.orders = []
      }
    },

    // Guardar órdenes en localStorage
    saveToLocalStorage() {
      try {
        localStorage.setItem('localOrders', JSON.stringify(this.orders))
        console.log('💾 Órdenes guardadas en localStorage:', this.orders.length)
      } catch (error) {
        console.error('❌ Error guardando órdenes en localStorage:', error)
      }
    },

    // Cargar todas las órdenes
    fetchOrders() {
      this.loadFromLocalStorage()
      console.log('🔄 Órdenes en store:', this.orders.length)
      return this.sortedOrders
    },

    clearError() {
      this.error = null
    }
  }
})