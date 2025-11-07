// store/cart.js - con modo desarrollo temporal
import { defineStore } from 'pinia';
import { cartService } from '../services/cartService';

export const useCartStore = defineStore('cart', {
  state: () => ({
    cartItems: [],
    isLoading: false,
    error: null,
    useLocalMode: true // Cambiar a false cuando el backend esté listo
  }),

  getters: {
    itemCount: (state) => {
      return state.cartItems.reduce((total, item) => total + (item.cantidad || 0), 0);
    },
    cartTotal: (state) => {
      const total = state.cartItems.reduce((total, item) => {
        const price = parseFloat(item.producto_precio || 0);
        const quantity = parseInt(item.cantidad || 0);
        return total + (price * quantity);
      }, 0);
      return total.toFixed(2);
    },
    isEmpty: (state) => state.cartItems.length === 0,
    
    getItemByProductId: (state) => (productId) => {
      return state.cartItems.find(item => item.producto_id == productId);
    }
  },

  actions: {
    async fetchCart() {
      this.isLoading = true;
      this.error = null;
      
      try {
        if (this.useLocalMode) {
          console.log('🔄 Modo local: Cargando carrito desde localStorage...');
          this.cartItems = this.getLocalCart();
        } else {
          console.log('🔄 Modo servidor: Cargando carrito desde el servidor...');
          const cartData = await cartService.getCart();
          this.cartItems = cartData;
        }
        console.log(`✅ Carrito cargado: ${this.cartItems.length} items`);
        
      } catch (error) {
        console.error('❌ Error cargando carrito:', error);
        this.error = error.message;
        this.cartItems = [];
      } finally {
        this.isLoading = false;
      }
    },

    async addItem(product, quantity = 1) {
      try {
        this.error = null;
        console.log('➕ Agregando producto al carrito:', product.nombre);
        
        // Validaciones básicas
        if (!product.id) {
          throw new Error('El producto no tiene ID válido');
        }

        if (product.stock <= 0) {
          throw new Error('Producto agotado');
        }

        if (quantity > product.stock) {
          throw new Error('No hay suficiente stock disponible');
        }
        
        // Verificar si el producto ya está en el carrito
        const existingItem = this.getItemByProductId(product.id);
        
        if (existingItem) {
          const newQuantity = existingItem.cantidad + quantity;
          if (newQuantity > product.stock) {
            throw new Error('No hay suficiente stock disponible');
          }
          return await this.updateItemQuantity(existingItem.id, newQuantity);
        }
        
        if (this.useLocalMode) {
          // Modo local: agregar directamente al estado
          console.log('🔄 Modo local: Agregando producto sin llamar al backend');
          const newItem = this.createCartItem(product, quantity);
          this.cartItems.push(newItem);
          this.saveLocalCart();
        } else {
          // Modo servidor: llamar al backend
          console.log('🔄 Modo servidor: Llamando al backend...');
          await cartService.addItemToCart(product.id, quantity);
          const newItem = this.createCartItem(product, quantity);
          this.cartItems.push(newItem);
        }
        
        console.log('✅ Producto agregado al carrito:', product.nombre);
        return true;
        
      } catch (error) {
        console.error('❌ Error agregando producto:', error);
        this.error = error.message;
        throw error;
      }
    },

    async removeCartItem(itemId) {
      try {
        this.error = null;
        console.log(`🗑️ Eliminando item del carrito: ${itemId}`);
        
        if (this.useLocalMode) {
          this.cartItems = this.cartItems.filter(item => item.id !== itemId);
          this.saveLocalCart();
        } else {
          await cartService.removeItem(itemId);
          this.cartItems = this.cartItems.filter(item => item.id !== itemId);
        }
        
        console.log('✅ Producto eliminado del carrito');
        
      } catch (error) {
        console.error('❌ Error eliminando producto:', error);
        this.error = error.message;
        throw error;
      }
    },

    async updateItemQuantity(itemId, quantity) {
      try {
        this.error = null;
        console.log(`🔄 Actualizando cantidad del item ${itemId} a ${quantity}`);
        
        if (quantity <= 0) {
          return await this.removeCartItem(itemId);
        }
        
        const item = this.cartItems.find(item => item.id === itemId);
        if (item) {
          if (quantity > item.producto_stock) {
            throw new Error('No hay suficiente stock disponible');
          }
          
          if (this.useLocalMode) {
            item.cantidad = quantity;
            item.subtotal = item.cantidad * item.producto_precio;
            this.saveLocalCart();
          } else {
            await cartService.updateQuantity(itemId, quantity);
            item.cantidad = quantity;
            item.subtotal = item.cantidad * item.producto_precio;
          }
        }
        
        console.log('✅ Cantidad actualizada');
        
      } catch (error) {
        console.error('❌ Error actualizando cantidad:', error);
        this.error = error.message;
        throw error;
      }
    },

    async clearCart() {
      try {
        this.error = null;
        console.log('🧹 Vaciando carrito...');
        
        if (this.useLocalMode) {
          this.cartItems = [];
          this.saveLocalCart();
        } else {
          await cartService.clearCart();
          this.cartItems = [];
        }
        
        console.log('✅ Carrito vaciado');
        
      } catch (error) {
        console.error('❌ Error vaciando carrito:', error);
        this.error = error.message;
        throw error;
      }
    },

    // Helper para crear item del carrito
    createCartItem(product, quantity) {
      return {
        id: `cart-${Date.now()}-${product.id}`,
        cantidad: quantity,
        producto_id: product.id,
        producto_nombre: product.nombre,
        producto_precio: parseFloat(product.precio),
        producto_imagen: this.getProductImageUrl(product),
        producto_stock: product.stock,
        subtotal: (parseFloat(product.precio) * quantity)
      };
    },

    // Helpers para localStorage (modo local)
    getLocalCart() {
      try {
        const cart = localStorage.getItem('localCart');
        return cart ? JSON.parse(cart) : [];
      } catch {
        return [];
      }
    },

    saveLocalCart() {
      try {
        localStorage.setItem('localCart', JSON.stringify(this.cartItems));
      } catch (error) {
        console.error('Error guardando carrito local:', error);
      }
    },

    getProductImageUrl(product) {
      const imagen = product.imagen || product.imagen_url;
      
      if (!imagen) {
        return '/placeholder-product.jpg';
      }
      
      if (imagen.startsWith('http')) {
        return imagen;
      }
      
      if (imagen.startsWith('/static/uploads/')) {
        return `http://localhost:5000${imagen}`;
      }
      
      if (!imagen.startsWith('/')) {
        return `http://localhost:5000/static/uploads/${imagen}`;
      }
      
      return `http://localhost:5000${imagen}`;
    },

    clearError() {
      this.error = null;
    },

    // Método para cambiar entre modos
    setLocalMode(enabled) {
      this.useLocalMode = enabled;
      console.log(`🔧 Modo ${enabled ? 'local' : 'servidor'} activado`);
    }
  }
});