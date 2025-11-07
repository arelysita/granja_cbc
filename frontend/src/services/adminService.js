import api from './api'

export const adminService = {
  async getDashboardStats() {
    const response = await api.get('/admin/dashboard/stats')
    return response.data
  },

  async getAllSales(params = {}) {
    const response = await api.get('/admin/sales', { params })
    return response.data
  },

  async updateSaleStatus(saleId, status) {
    const response = await api.put(`/admin/sales/${saleId}/status`, {
      estado: status
    })
    return response.data
  },

  async getAllUsers() {
    const response = await api.get('/admin/users')
    return response.data
  },

  async getPendingReviews() {
    const response = await api.get('/admin/reviews/pending')
    return response.data
  },

  async approveReview(reviewId) {
    const response = await api.put(`/admin/reviews/${reviewId}/approve`)
    return response.data
  },

  async addStockMovement(movementData) {
    const response = await api.post('/admin/stock/movements', movementData)
    return response.data
  },

  async getSalesByCategory() {
    const response = await api.get('/admin/reports/sales-by-category')
    return response.data
  }
}