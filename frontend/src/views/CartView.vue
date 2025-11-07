<template>
  <div class="cart">
    <div class="container">
      <!-- Header Mejorado -->
      <div class="cart-header">
        <div class="header-main">
          <h1>🛒 Mi Carrito de Compras</h1>
          <div class="header-actions">
            <button 
              @click="clearCartWithConfirm" 
              class="btn-clear-all-header"
              :disabled="processingAction || isEmpty"
            >
              <span class="btn-icon">🗑️</span>
              Vaciar Carrito
            </button>
            <button @click="refreshCart" class="btn-refresh" title="Actualizar carrito">
              🔄
            </button>
          </div>
        </div>
        
        <div v-if="!isEmpty" class="cart-stats">
          <div class="stat-item">
            <span class="stat-label">Productos:</span>
            <span class="stat-value">{{ cartItems.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Unidades:</span>
            <span class="stat-value">{{ cartStore.itemCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Total:</span>
            <span class="stat-value total">${{ formatPrice(cartStore.cartTotal) }}</span>
          </div>
        </div>
      </div>

      <!-- Estado de Carga -->
      <div v-if="cartStore.isLoading" class="loading-state">
        <div class="spinner"></div>
        <p>Cargando tu carrito...</p>
      </div>

      <!-- Error del Servidor -->
      <div v-else-if="serverError" class="error-state">
        <div class="error-illustration">
          <div class="error-icon">⚠️</div>
          <div class="error-animation">
            <div class="pulse-dot"></div>
            <div class="pulse-dot"></div>
            <div class="pulse-dot"></div>
          </div>
        </div>
        <div class="error-content">
          <h2>Problema de conexión</h2>
          <p>No pudimos cargar tu carrito. Esto puede ser temporal.</p>
          <div class="error-details" v-if="showErrorDetails">
            <p><strong>Detalles técnicos:</strong></p>
            <p>{{ serverError.message }}</p>
            <p v-if="serverError.code">Código: {{ serverError.code }}</p>
          </div>
          <div class="error-actions">
            <button @click="retryLoadCart" class="btn btn-primary">
              <span class="btn-icon">🔄</span>
              Reintentar
            </button>
            <button @click="useLocalCart" class="btn btn-secondary">
              <span class="btn-icon">🛒</span>
              Usar Carrito Local
            </button>
            <button @click="showErrorDetails = !showErrorDetails" class="btn btn-text">
              {{ showErrorDetails ? 'Ocultar' : 'Mostrar' }} detalles
            </button>
          </div>
        </div>
      </div>

      <!-- Carrito Vacío -->
      <div v-else-if="isEmpty" class="empty-cart">
        <div class="empty-cart-illustration">
          <div class="empty-cart-icon">🛒</div>
          <div class="empty-cart-animation">
            <div class="bounce-item">📦</div>
            <div class="bounce-item">🍎</div>
            <div class="bounce-item">🥦</div>
          </div>
        </div>
        <div class="empty-cart-content">
          <h2>Tu carrito está vacío</h2>
          <p>¡Descubre nuestros productos frescos y agrégalos a tu carrito!</p>
          <div class="empty-actions">
            <router-link to="/products" class="btn btn-primary btn-large">
              <span class="btn-icon">🔍</span>
              Explorar Productos
            </router-link>
            <button @click="refreshCart" class="btn btn-secondary">
              <span class="btn-icon">🔄</span>
              Actualizar
            </button>
          </div>
        </div>
      </div>

      <!-- Carrito con Productos -->
      <div v-else class="cart-content">
        <!-- Alertas Importantes -->
        <div v-if="hasLowStockItems" class="alert-low-stock">
          <div class="alert-icon">⚠️</div>
          <div class="alert-content">
            <strong>Atención:</strong> 
            Tienes {{ lowStockCount }} producto(s) con stock bajo. 
            Te recomendamos finalizar tu compra pronto.
          </div>
        </div>

        <div class="cart-layout">
          <!-- Lista de Productos Mejorada -->
          <div class="cart-items-section">
            <div class="section-header">
              <h2>📦 Tus Productos Seleccionados</h2>
              <div class="section-stats">
                <span class="items-count">{{ cartStore.itemCount }} unidades</span>
              </div>
            </div>

            <div class="cart-items-list">
              <div 
                v-for="item in cartItems" 
                :key="item.id" 
                class="cart-item-card"
                :class="{ 
                  'low-stock-item': item.producto_stock <= 3,
                  'medium-stock': item.producto_stock <= 10 
                }"
              >
                <!-- Imagen del Producto -->
                <div class="item-image-container">
                  <img 
                    :src="getProductImage(item)" 
                    :alt="item.producto_nombre"
                    class="item-image"
                    @error="handleImageError"
                  >
                  <div v-if="item.producto_stock <= 3" class="stock-badge critical">
                    <span class="badge-icon">🔥</span>
                    Stock Crítico
                  </div>
                  <div v-else-if="item.producto_stock <= 10" class="stock-badge warning">
                    <span class="badge-icon">⚠️</span>
                    Stock Bajo
                  </div>
                </div>
                
                <!-- Información del Producto -->
                <div class="item-info">
                  <h3 class="product-name">{{ item.producto_nombre }}</h3>
                  <p class="product-price">${{ formatPrice(item.producto_precio) }} c/u</p>
                  
                  <div class="product-details">
                    <div class="detail-item">
                      <span class="detail-label">Cantidad:</span>
                      <span class="detail-value">{{ item.cantidad }} unidades</span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">Disponible:</span>
                      <span class="detail-value">{{ item.producto_stock }} unidades</span>
                    </div>
                    <div class="detail-item">
                      <span class="detail-label">SKU:</span>
                      <span class="detail-value">#{{ item.producto_id }}</span>
                    </div>
                  </div>
                </div>

                <!-- Subtotal y Acciones -->
                <div class="item-summary">
                  <div class="subtotal-info">
                    <div class="subtotal-amount">
                      ${{ formatPrice(item.cantidad * item.producto_precio) }}
                    </div>
                    <div class="unit-price">
                      ${{ formatPrice(item.producto_precio) }} c/u
                    </div>
                  </div>
                  
                  <div class="item-actions">
                    <button 
                      @click="removeItem(item)"
                      class="action-btn remove"
                      :disabled="processingAction"
                      title="Eliminar producto"
                    >
                      <span class="action-icon">🗑️</span>
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Promociones y Ofertas -->
            <div class="promotions-section">
              <div class="promotion-card">
                <div class="promotion-icon">🎁</div>
                <div class="promotion-content">
                  <h4>¡Envío Gratis!</h4>
                  <p>Agrega ${{ formatPrice(50000 - parseFloat(cartStore.cartTotal)) }} más a tu carrito para obtener envío gratis</p>
                  <div class="promotion-progress">
                    <div class="progress-bar">
                      <div 
                        class="progress-fill" 
                        :style="{ width: `${shippingProgress}%` }"
                      ></div>
                    </div>
                    <span class="progress-text">{{ Math.round(shippingProgress) }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Resumen del Pedido Mejorado -->
          <div class="cart-summary-section">
            <div class="summary-card">
              <div class="summary-header">
                <h3 class="summary-title">✅ Resumen de Compra</h3>
                <div class="secure-badge">
                  <span class="secure-icon">🛡️</span>
                  Compra Segura
                </div>
              </div>
              
              <div class="summary-details">
                <!-- Productos -->
                <div class="summary-group">
                  <div class="group-title">Productos</div>
                  <div class="summary-row">
                    <span>Subtotal ({{ cartStore.itemCount }} items):</span>
                    <span>${{ formatPrice(cartStore.cartTotal) }}</span>
                  </div>
                </div>

                <!-- Envío -->
                <div class="summary-group">
                  <div class="group-title">Envío</div>
                  <div class="summary-row">
                    <span>Costo de envío:</span>
                    <span v-if="parseFloat(cartStore.cartTotal) > 50000" class="free-shipping">
                      <span class="shipping-icon">🚚</span>
                      GRATIS
                    </span>
                    <span v-else>$5.000</span>
                  </div>
                  <div v-if="parseFloat(cartStore.cartTotal) <= 50000" class="shipping-savings">
                    <span class="savings-icon">💸</span>
                    Ahorras $5.000 agregando ${{ formatPrice(50000 - parseFloat(cartStore.cartTotal)) }} más
                  </div>
                </div>

                <!-- Descuentos -->
                <div class="summary-group">
                  <div class="group-title">Ahorros</div>
                  <div class="summary-row discount">
                    <span>Envío gratis:</span>
                    <span class="discount-amount">-$5.000</span>
                  </div>
                </div>

                <div class="summary-divider"></div>
                
                <!-- Total -->
                <div class="summary-group total-group">
                  <div class="summary-row total-row">
                    <span>
                      <strong>Total Final</strong>
                      <small>(incluye IVA)</small>
                    </span>
                    <span class="total-amount">
                      ${{ formatPrice(totalWithShipping) }}
                    </span>
                  </div>
                  <div class="total-savings">
                    <span class="savings-badge">¡Ahorras $5.000!</span>
                  </div>
                </div>
              </div>

              <!-- Acciones Principales -->
              <div class="summary-actions">
                <!-- Botón Principal VERDE -->
                <button 
                  @click="proceedToCheckout"
                  class="btn-checkout-primary"
                  :disabled="processingCheckout || cartStore.isLoading || serverError"
                >
                  <div class="checkout-content">
                    <div class="checkout-main">
                      <span class="checkout-icon">🚀</span>
                      <span class="checkout-text">FINALIZAR COMPRA</span>
                    </div>
                    <div class="checkout-subtitle">
                      Total: ${{ formatPrice(totalWithShipping) }}
                    </div>
                  </div>
                  <div class="checkout-security">
                    <span class="security-icon">🔒</span>
                    Pago 100% seguro
                  </div>
                </button>

                <!-- Acciones Secundarias -->
                <div class="secondary-actions">
                  <button 
                    @click="continueShopping"
                    class="btn-continue-shopping"
                  >
                    <span class="btn-icon">←</span>
                    Seguir Comprando
                  </button>
                </div>
              </div>

              <!-- Garantías y Beneficios -->
              <div class="benefits-section">
                <div class="benefits-grid">
                  <div class="benefit-item">
                    <span class="benefit-icon">🛡️</span>
                    <div class="benefit-content">
                      <strong>Garantía de Calidad</strong>
                      <span>Productos 100% frescos</span>
                    </div>
                  </div>
                  <div class="benefit-item">
                    <span class="benefit-icon">🚚</span>
                    <div class="benefit-content">
                      <strong>Entrega Rápida</strong>
                      <span>24-48 horas</span>
                    </div>
                  </div>
                  <div class="benefit-item">
                    <span class="benefit-icon">↩️</span>
                    <div class="benefit-content">
                      <strong>Devoluciones</strong>
                      <span>30 días garantizados</span>
                    </div>
                  </div>
                  <div class="benefit-item">
                    <span class="benefit-icon">📞</span>
                    <div class="benefit-content">
                      <strong>Soporte</strong>
                      <span>24/7 disponible</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notificación de Éxito -->
      <div v-if="showSuccessToast" class="success-toast">
        <div class="toast-content">
          <span class="toast-icon">✅</span>
          <span class="toast-message">{{ successMessage }}</span>
        </div>
        <button @click="showSuccessToast = false" class="toast-close">
          <span class="close-icon">×</span>
        </button>
      </div>

      <!-- Notificación de Error del Store -->
      <div v-if="cartStore.error && !serverError" class="error-notification">
        <div class="error-content">
          <span class="error-icon">⚠️</span>
          <div class="error-details">
            <h4>Error en el carrito</h4>
            <p>{{ cartStore.error.message || cartStore.error }}</p>
          </div>
          <button @click="cartStore.clearError()" class="error-close">
            <span class="close-icon">×</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../store/cart'
import { useAuthStore } from '../store/auth'

// Servicios de API mejorados
const fetchCartAPI = async () => {
  try {
    const response = await fetch('/api/cart/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en fetchCartAPI:', error);
    throw error;
  }
};

const removeCartItemAPI = async (itemId) => {
  try {
    const response = await fetch(`/api/cart/${itemId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en removeCartItemAPI:', error);
    throw error;
  }
};

const clearCartAPI = async () => {
  try {
    const response = await fetch('/api/cart/clear', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include'
    });

    if (!response.ok) {
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error en clearCartAPI:', error);
    throw error;
  }
};

export default {
  name: 'CartView',
  setup() {
    const cartStore = useCartStore()
    const authStore = useAuthStore()
    const router = useRouter()
    
    const processingAction = ref(false)
    const processingCheckout = ref(false)
    const showSuccessToast = ref(false)
    const successMessage = ref('')
    const serverError = ref(null)
    const showErrorDetails = ref(false)
    const usingLocalCart = ref(false)

    // Computed properties
    const cartItems = computed(() => {
      if (usingLocalCart.value) {
        return getLocalCartItems()
      }
      return cartStore.cartItems || []
    })
    
    const isEmpty = computed(() => {
      if (usingLocalCart.value) {
        const localItems = getLocalCartItems()
        return !localItems || localItems.length === 0
      }
      return !cartStore.cartItems || cartStore.cartItems.length === 0
    })
    
    const totalWithShipping = computed(() => {
      const subtotal = parseFloat(cartStore.cartTotal || 0)
      const shipping = subtotal > 50000 ? 0 : 5000
      return subtotal + shipping
    })

    const shippingProgress = computed(() => {
      const subtotal = parseFloat(cartStore.cartTotal || 0)
      return Math.min((subtotal / 50000) * 100, 100)
    })

    const hasLowStockItems = computed(() => {
      return cartItems.value.some(item => item.producto_stock <= 5)
    })

    const lowStockCount = computed(() => {
      return cartItems.value.filter(item => item.producto_stock <= 5).length
    })

    // Funciones para carrito local
    const getLocalCartItems = () => {
      try {
        const localCart = localStorage.getItem('localCart')
        return localCart ? JSON.parse(localCart) : []
      } catch {
        return []
      }
    }

    const saveLocalCartItems = (items) => {
      try {
        localStorage.setItem('localCart', JSON.stringify(items))
      } catch (error) {
        console.error('Error guardando carrito local:', error)
      }
    }

    const useLocalCart = () => {
      usingLocalCart.value = true
      serverError.value = null
      showToast('Usando carrito local temporalmente')
    }

    // Métodos de utilidad
    const formatPrice = (price) => {
      const number = parseFloat(price)
      return isNaN(number) ? '0' : number.toLocaleString('es-ES')
    }

    const getProductImage = (item) => {
      if (!item.producto_imagen) {
        return '/placeholder-product.jpg'
      }
      
      if (item.producto_imagen.startsWith('http')) {
        return item.producto_imagen
      }
      
      const baseUrl = 'http://localhost:5000'
      let imagePath = item.producto_imagen
      
      if (imagePath.startsWith('/')) {
        imagePath = imagePath.slice(1)
      }
      
      if (!imagePath.includes('uploads/') && !imagePath.includes('static/')) {
        imagePath = `static/uploads/${imagePath}`
      }
      
      return `${baseUrl}/${imagePath}`
    }

    const showToast = (message) => {
      successMessage.value = message
      showSuccessToast.value = true
      setTimeout(() => {
        showSuccessToast.value = false
      }, 5000)
    }

    // Operaciones del carrito - MEJORADAS
    const removeItem = async (item) => {
      if (!confirm(`¿Eliminar "${item.producto_nombre}" del carrito?`)) return
      
      processingAction.value = true
      try {
        if (usingLocalCart.value) {
          // Eliminar del carrito local
          const currentItems = getLocalCartItems()
          const updatedItems = currentItems.filter(i => i.id !== item.id)
          saveLocalCartItems(updatedItems)
        } else {
          // Eliminar del servidor
          await cartStore.removeCartItem(item.id)
        }
        showToast(`${item.producto_nombre} eliminado del carrito`)
      } catch (error) {
        console.error('Error eliminando producto:', error)
        alert('Error eliminando producto del carrito')
      } finally {
        processingAction.value = false
      }
    }

    const clearCartWithConfirm = async () => {
      if (!confirm('¿Estás seguro de que quieres vaciar todo el carrito? Esta acción no se puede deshacer.')) return
      
      processingAction.value = true
      try {
        if (usingLocalCart.value) {
          saveLocalCartItems([])
        } else {
          await cartStore.clearCart()
        }
        showToast('Carrito vaciado correctamente')
      } catch (error) {
        console.error('Error vaciando carrito:', error)
        alert('Error vaciando carrito')
      } finally {
        processingAction.value = false
      }
    }

    const refreshCart = async () => {
      try {
        serverError.value = null
        usingLocalCart.value = false
        await cartStore.fetchCart()
        showToast('Carrito actualizado')
      } catch (error) {
        console.error('Error refrescando carrito:', error)
        serverError.value = {
          message: error.message,
          code: error.response?.status
        }
      }
    }

    const retryLoadCart = async () => {
      await refreshCart()
    }

    const proceedToCheckout = async () => {
      processingCheckout.value = true
      try {
        // Validar autenticación
        if (!authStore.isAuthenticated) {
          router.push('/login?redirect=checkout')
          return
        }

        // Validar stock crítico
        const criticalStockItems = cartItems.value.filter(item => item.producto_stock <= 2)
        if (criticalStockItems.length > 0) {
          const productNames = criticalStockItems.map(item => item.producto_nombre).join(', ')
          if (!confirm(`⚠️ Los siguientes productos tienen stock MUY bajo: ${productNames}. ¿Continuar con la compra?`)) {
            return
          }
        }

        // Redirigir a checkout
        router.push('/checkout')
        
      } catch (error) {
        console.error('Error en checkout:', error)
        alert('Error procesando el checkout')
      } finally {
        processingCheckout.value = false
      }
    }

    const continueShopping = () => {
      router.push('/products')
    }

    const handleImageError = (event) => {
      event.target.src = '/placeholder-product.jpg'
    }

    // Lifecycle
    onMounted(async () => {
      try {
        await cartStore.fetchCart()
      } catch (error) {
        console.error('Error cargando carrito inicial:', error)
        serverError.value = {
          message: error.message,
          code: error.response?.status
        }
        
        // Intentar cargar carrito local como fallback
        const localItems = getLocalCartItems()
        if (localItems.length > 0) {
          usingLocalCart.value = true
          showToast('Cargado carrito local temporalmente')
        }
      }
    })

    return {
      cartStore,
      cartItems,
      isEmpty,
      totalWithShipping,
      shippingProgress,
      hasLowStockItems,
      lowStockCount,
      processingAction,
      processingCheckout,
      showSuccessToast,
      successMessage,
      serverError,
      showErrorDetails,
      removeItem,
      clearCartWithConfirm,
      refreshCart,
      retryLoadCart,
      useLocalCart,
      proceedToCheckout,
      continueShopping,
      handleImageError,
      formatPrice,
      getProductImage
    }
  }
}
</script>

<style scoped>
/* COLORES CORREGIDOS - TODOS VISIBLES */
:root {
  --primary-green: #27ae60;
  --green-dark: #219a52;
  --green-light: #58d68d;
  --green-bg: #e8f5e8;
  --text-dark: #2c3e50;
  --text-medium: #34495e;
  --text-light: #5d6d7e;
  --white: #ffffff;
  --light-gray: #f8f9fa;
  --medium-gray: #e9ecef;
  --dark-gray: #6c757d;
  --border-radius: 12px;
  --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

.cart {
  padding: 2rem 0;
  background: var(--light-gray);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header Mejorado */
.cart-header {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  margin-bottom: 2rem;
  overflow: hidden;
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--medium-gray);
}

.cart-header h1 {
  color: var(--text-dark);
  font-size: 2.2rem;
  margin: 0;
  font-weight: 700;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-clear-all-header {
  background: #e74c3c;
  color: var(--white);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: var(--transition);
}

.btn-clear-all-header:hover:not(:disabled) {
  background: #c0392b;
  transform: translateY(-1px);
}

.btn-clear-all-header:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-refresh {
  background: var(--medium-gray);
  border: none;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 1.1rem;
  transition: var(--transition);
  color: var(--text-dark);
}

.btn-refresh:hover {
  background: var(--dark-gray);
  color: var(--white);
}

.cart-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  padding: 1.5rem 2rem;
  background: var(--green-bg);
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--white);
  border-radius: var(--border-radius);
  border: 1px solid var(--green-light);
}

.stat-label {
  color: var(--text-dark);
  font-weight: 600;
}

.stat-value {
  color: var(--text-dark);
  font-weight: 700;
  font-size: 1.1rem;
}

.stat-value.total {
  color: var(--primary-green);
  font-size: 1.3rem;
}

/* Estados */
.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-dark);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--medium-gray);
  border-top: 4px solid var(--primary-green);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Estado de Error Mejorado */
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4rem 2rem;
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  border: 2px solid #e74c3c;
}

.error-illustration {
  position: relative;
  margin-bottom: 2rem;
}

.error-icon {
  font-size: 4rem;
  color: #e74c3c;
  margin-bottom: 1rem;
}

.error-animation {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #e74c3c;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

.pulse-dot:nth-child(2) {
  animation-delay: 0.3s;
}

.pulse-dot:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.error-state h2 {
  color: var(--text-dark);
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.error-state p {
  color: var(--text-dark);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.error-details {
  background: var(--light-gray);
  padding: 1rem;
  border-radius: var(--border-radius);
  margin-bottom: 1.5rem;
  text-align: left;
  max-width: 500px;
}

.error-details p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.error-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

/* Carrito Vacío Mejorado */
.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4rem 2rem;
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.empty-cart-illustration {
  position: relative;
  margin-bottom: 2rem;
}

.empty-cart-icon {
  font-size: 6rem;
  opacity: 0.7;
  margin-bottom: 1rem;
}

.empty-cart-animation {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.bounce-item {
  font-size: 2rem;
  animation: bounce 2s infinite;
}

.bounce-item:nth-child(2) {
  animation-delay: 0.2s;
}

.bounce-item:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-cart h2 {
  color: var(--text-dark);
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.empty-cart p {
  color: var(--text-dark);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.empty-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

/* Layout del Carrito */
.cart-content {
  margin-top: 2rem;
}

.cart-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* Alertas */
.alert-low-stock {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: var(--border-radius);
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.alert-icon {
  font-size: 1.5rem;
}

.alert-content {
  flex: 1;
  color: #856404;
}

/* Sección de Items */
.cart-items-section {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--medium-gray);
  background: var(--light-gray);
}

.section-header h2 {
  color: var(--text-dark);
  margin: 0;
  font-size: 1.4rem;
}

.section-stats {
  color: var(--text-dark);
  font-weight: 600;
}

/* Lista de Items */
.cart-items-list {
  padding: 1rem;
}

.cart-item-card {
  display: grid;
  grid-template-columns: 100px 1fr auto;
  gap: 1.5rem;
  align-items: center;
  padding: 1.5rem;
  background: var(--white);
  border: 1px solid var(--medium-gray);
  border-radius: var(--border-radius);
  margin-bottom: 1rem;
  transition: var(--transition);
}

.cart-item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.cart-item-card.low-stock-item {
  border-left: 4px solid #e74c3c;
  background: #fff5f5;
}

.cart-item-card.medium-stock {
  border-left: 4px solid #f39c12;
  background: #fffaf0;
}

/* Imagen del Producto */
.item-image-container {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: var(--border-radius);
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stock-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--white);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.stock-badge.critical {
  background: #e74c3c;
}

.stock-badge.warning {
  background: #f39c12;
}

/* Información del Producto */
.item-info {
  flex: 1;
}

.product-name {
  font-weight: 600;
  color: var(--text-dark);
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  line-height: 1.4;
}

.product-price {
  color: var(--primary-green);
  font-weight: 600;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.detail-label {
  color: var(--text-dark);
  font-weight: 600;
}

.detail-value {
  color: var(--text-dark);
  font-weight: 500;
}

/* Subtotal y Acciones */
.item-summary {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1rem;
  min-width: 140px;
}

.subtotal-info {
  text-align: right;
}

.subtotal-amount {
  font-weight: 700;
  color: var(--text-dark);
  font-size: 1.3rem;
}

.unit-price {
  font-size: 0.85rem;
  color: var(--text-dark);
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: var(--medium-gray);
  color: var(--text-dark);
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: var(--transition);
}

.action-btn:hover:not(:disabled) {
  background: var(--dark-gray);
  color: var(--white);
}

.action-btn.remove:hover {
  background: #e74c3c;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Promociones */
.promotions-section {
  padding: 1rem;
  border-top: 1px solid var(--medium-gray);
}

.promotion-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, var(--primary-green), var(--green-dark));
  border-radius: var(--border-radius);
  color: var(--white);
}

.promotion-icon {
  font-size: 2rem;
}

.promotion-content h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.promotion-content p {
  margin: 0 0 0.5rem 0;
  opacity: 0.9;
}

.promotion-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.progress-bar {
  flex: 1;
  height: 6px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--white);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.8rem;
  font-weight: 600;
}

/* Resumen del Pedido - CORREGIDO PARA VISIBILIDAD */
.cart-summary-section {
  position: sticky;
  top: 2rem;
}

.summary-card {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.summary-header {
  background: var(--primary-green);
  color: var(--white);
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.summary-title {
  margin: 0;
  font-size: 1.3rem;
  color: var(--white);
}

.secure-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.9;
  color: var(--white);
}

.summary-details {
  padding: 1.5rem 2rem;
}

.summary-group {
  margin-bottom: 1.5rem;
}

.group-title {
  font-weight: 600;
  color: var(--text-dark) !important;
  margin-bottom: 0.75rem;
  font-size: 1rem;
  border-bottom: 1px solid var(--medium-gray);
  padding-bottom: 0.5rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  color: var(--text-dark) !important;
}

.summary-row.discount {
  color: var(--primary-green) !important;
}

.discount-amount {
  font-weight: 600;
  color: var(--primary-green) !important;
}

.shipping-savings {
  background: var(--green-bg);
  border: 1px solid var(--green-light);
  border-radius: var(--border-radius);
  padding: 0.75rem;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--primary-green) !important;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.free-shipping {
  color: var(--primary-green) !important;
  font-weight: 800;
}

.summary-divider {
  height: 2px;
  background: var(--medium-gray);
  margin: 1.5rem 0;
}

.total-group {
  background: var(--green-bg);
  margin: -1.5rem -2rem -1.5rem -2rem;
  padding: 1.5rem 2rem;
}

.total-row {
  font-weight: 700;
  font-size: 1.4rem;
  color: var(--text-dark) !important;
}

.total-amount {
  font-size: 1.6rem;
  color: var(--primary-green) !important;
}

.total-savings {
  text-align: center;
  margin-top: 0.5rem;
}

.savings-badge {
  background: var(--primary-green);
  color: var(--white) !important;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

/* Acciones del Resumen */
.summary-actions {
  padding: 0 2rem 2rem;
}

/* BOTÓN PRINCIPAL VERDE GRANDE */
.btn-checkout-primary {
  width: 100%;
  background: linear-gradient(135deg, var(--primary-green), var(--green-dark));
  color: var(--white);
  border: none;
  padding: 1.5rem 2rem;
  border-radius: var(--border-radius);
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  margin-bottom: 1rem;
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
}

.btn-checkout-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(39, 174, 96, 0.6);
}

.btn-checkout-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.checkout-content {
  text-align: center;
  margin-bottom: 0.5rem;
}

.checkout-main {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  margin-bottom: 0.25rem;
}

.checkout-subtitle {
  font-size: 1rem;
  opacity: 0.9;
  font-weight: 600;
}

.checkout-security {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.9;
}

.secondary-actions {
  display: flex;
  gap: 1rem;
}

.btn-continue-shopping {
  flex: 1;
  background: var(--medium-gray);
  color: var(--text-dark) !important;
  border: none;
  padding: 1rem 1.5rem;
  border-radius: var(--border-radius);
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-continue-shopping:hover {
  background: var(--dark-gray);
  color: var(--white) !important;
}

/* Beneficios */
.benefits-section {
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--medium-gray);
  background: var(--light-gray);
}

.benefits-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.benefit-icon {
  font-size: 1.5rem;
}

.benefit-content {
  display: flex;
  flex-direction: column;
}

.benefit-content strong {
  color: var(--text-dark);
  font-size: 0.9rem;
}

.benefit-content span {
  color: var(--text-dark);
  font-size: 0.8rem;
}

/* Notificaciones */
.success-toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  background: var(--primary-green);
  color: var(--white);
  padding: 1rem 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
  z-index: 1000;
  animation: slideIn 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-notification {
  position: fixed;
  top: 2rem;
  right: 2rem;
  background: #e74c3c;
  color: var(--white);
  padding: 1rem 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
  z-index: 1000;
  animation: slideIn 0.3s ease;
}

.error-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.error-details h4 {
  margin: 0 0 0.25rem 0;
  font-size: 1rem;
  color: var(--white);
}

.error-details p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
  color: var(--white);
}

.error-close,
.toast-close {
  background: none;
  border: none;
  color: var(--white);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0;
  margin-left: 0.5rem;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Botones Generales */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: var(--transition);
  font-size: 1rem;
}

.btn-primary {
  background: var(--primary-green);
  color: var(--white);
}

.btn-primary:hover:not(:disabled) {
  background: var(--green-dark);
}

.btn-secondary {
  background: var(--dark-gray);
  color: var(--white);
}

.btn-secondary:hover:not(:disabled) {
  background: #5a6268;
}

.btn-text {
  background: transparent;
  color: var(--text-dark);
  text-decoration: underline;
}

.btn-text:hover {
  background: var(--medium-gray);
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1.1rem;
}

.btn-icon {
  margin-right: 0.5rem;
}

/* Responsive */
@media (max-width: 968px) {
  .cart-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .cart-summary-section {
    position: static;
  }
  
  .benefits-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-main {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .cart-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .cart-item-card {
    grid-template-columns: 80px 1fr;
    gap: 1rem;
  }
  
  .item-summary {
    grid-column: 1 / -1;
    justify-self: end;
    flex-direction: row;
    align-items: center;
  }
  
  .secondary-actions {
    flex-direction: column;
  }
  
  .success-toast,
  .error-notification {
    right: 1rem;
    left: 1rem;
  }
  
  .error-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.5rem;
  }
  
  .cart-header,
  .section-header,
  .summary-header {
    padding: 1rem;
  }
  
  .summary-details,
  .summary-actions {
    padding: 1rem;
  }
  
  .checkout-main {
    font-size: 1.1rem;
  }
}
</style>