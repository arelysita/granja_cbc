import api from './api'

export const saleService = {
  async createSale(saleData) {
    const response = await api.post('/sales', saleData)
    return response.data
  },

  async getMyOrders() {
    const response = await api.get('/sales/my-orders')
    return response.data
  },

  async getOrder(id) {
    const response = await api.get(`/sales/${id}`)
    return response.data
  }
}