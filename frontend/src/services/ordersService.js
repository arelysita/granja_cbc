import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  withCredentials: true,
});

export const ordersService = {
  /**
   * Obtener todas las órdenes del usuario
   */
  async getOrders() {
    try {
      console.log('🔄 Obteniendo órdenes del usuario...');
      const response = await apiClient.get('/orders');
      console.log('✅ Órdenes obtenidas correctamente');
      return response.data;
    } catch (error) {
      console.error('❌ Error detallado obteniendo órdenes:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message
      });
      
      // Si es error 422, probablemente es un problema de validación o el usuario no tiene órdenes
      if (error.response?.status === 422) {
        console.log('📭 El usuario no tiene órdenes o hay problema de validación');
        return [];
      }
      
      // Si es 404, el endpoint no existe
      if (error.response?.status === 404) {
        console.log('🔍 Endpoint de órdenes no encontrado');
        return [];
      }
      
      // Si es 401, no autenticado
      if (error.response?.status === 401) {
        console.log('🔐 No autenticado para ver órdenes');
        throw new Error('No estás autenticado para ver las órdenes');
      }
      
      throw error;
    }
  },

  /**
   * Crear una nueva orden
   */
  async createOrder(orderData) {
    try {
      console.log('🔄 Creando nueva orden...');
      
      const response = await apiClient.post('/orders', orderData);
      console.log('✅ Orden creada exitosamente');
      return response.data;
      
    } catch (error) {
      console.error('❌ Error detallado creando orden:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        message: error.message
      });
      
      if (error.response?.status === 422) {
        const validationErrors = error.response?.data;
        console.error('📋 Errores de validación específicos:', validationErrors);
        throw new Error(`Error de validación: ${JSON.stringify(validationErrors)}`);
      }
      
      throw new Error('No se pudo crear la orden: ' + error.message);
    }
  },

  /**
   * Obtener una orden específica
   */
  async getOrder(orderId) {
    try {
      console.log(`🔄 Obteniendo orden ${orderId}...`);
      const response = await apiClient.get(`/orders/${orderId}`);
      return response.data;
    } catch (error) {
      console.error('❌ Error obteniendo orden:', error);
      throw error;
    }
  }
};

export default ordersService;