// cartService.js - con debug mejorado
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  withCredentials: true,
});

// Interceptor para debug
apiClient.interceptors.request.use(
  (config) => {
    console.log('🚀 Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      data: config.data,
      headers: config.headers
    });
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    return Promise.reject(error);
  }
);

export const cartService = {
  async getCart() {
    try {
      console.log('🔄 Obteniendo carrito...');
      const response = await apiClient.get('/cart/');
      return this.transformCartData(response.data);
    } catch (error) {
      console.error('❌ Error obteniendo carrito:', error.message);
      return [];
    }
  },

  async addItemToCart(productId, quantity = 1) {
    try {
      console.log(`🛒 Agregando producto ID: ${productId}, cantidad: ${quantity}`);
      
      // Preparar datos para el backend - diferentes formatos posibles
      const requestData = {
        // Intentar diferentes nombres de campo que el backend pueda esperar
        product_id: productId,
        producto_id: productId,
        productId: productId,
        id: productId,
        quantity: quantity,
        cantidad: quantity
      };
      
      console.log('📤 Enviando datos al backend:', requestData);
      
      const response = await apiClient.post('/cart/add', requestData);
      
      console.log('✅ Producto agregado al carrito');
      return response.data;
      
    } catch (error) {
      console.error('❌ Error agregando al carrito:', error);
      
      // Mostrar detalles del error 422
      if (error.response?.status === 422) {
        const validationErrors = error.response?.data;
        console.error('📋 Errores de validación:', validationErrors);
        throw new Error(`Error de validación: ${JSON.stringify(validationErrors)}`);
      }
      
      throw new Error('No se pudo agregar el producto al carrito: ' + error.message);
    }
  },

  async removeItem(itemId) {
    try {
      console.log(`🗑️ Eliminando item ${itemId}...`);
      const response = await apiClient.delete(`/cart/${itemId}`);
      return response.data;
    } catch (error) {
      console.error('❌ Error eliminando item:', error.message);
      throw new Error('No se pudo eliminar el producto del carrito: ' + error.message);
    }
  },

  async clearCart() {
    try {
      console.log('🧹 Vaciando carrito...');
      const response = await apiClient.post('/cart/clear');
      return response.data;
    } catch (error) {
      console.error('❌ Error vaciando carrito:', error.message);
      throw new Error('No se pudo vaciar el carrito: ' + error.message);
    }
  },

  transformCartData(cartData) {
    if (!cartData) return [];
    
    if (Array.isArray(cartData)) {
      return cartData.map(item => this.transformCartItem(item)).filter(Boolean);
    }
    
    if (cartData.items && Array.isArray(cartData.items)) {
      return cartData.items.map(item => this.transformCartItem(item)).filter(Boolean);
    }
    
    return [];
  },

  transformCartItem(item) {
    if (!item) return null;

    return {
      id: item.id || item.cart_item_id || `temp-${Date.now()}`,
      cantidad: item.cantidad || item.quantity || 1,
      producto_id: item.producto_id || item.product_id,
      producto_nombre: item.producto_nombre || item.product_name || 'Producto',
      producto_precio: parseFloat(item.producto_precio || item.product_price || 0),
      producto_imagen: item.producto_imagen || item.product_image || '/placeholder-product.jpg',
      producto_stock: item.producto_stock || item.product_stock || 0,
      subtotal: (item.cantidad || 1) * parseFloat(item.producto_precio || 0)
    };
  }
};

export default cartService;