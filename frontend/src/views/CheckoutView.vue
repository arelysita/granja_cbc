<template>
  <div class="checkout-view">
    <div class="container">
      <!-- Header -->
      <div class="checkout-header">
        <h1>🛒 Finalizar Compra</h1>
        <router-link to="/cart" class="back-to-cart">
          ← Volver al Carrito
        </router-link>
      </div>

      <!-- Contenido principal -->
      <div class="checkout-content" v-if="!isEmpty">
        <div class="checkout-layout">
          <!-- Formulario de envío y pago -->
          <div class="checkout-form-section">
            <div class="form-section">
              <h2>📦 Información de Envío</h2>
              <form @submit.prevent="processCheckout" class="checkout-form">
                <div class="form-group">
                  <label for="nombre">Nombre completo *</label>
                  <input
                    type="text"
                    id="nombre"
                    v-model="formData.nombre"
                    required
                    placeholder="Ingresa tu nombre completo"
                  >
                </div>

                <div class="form-group">
                  <label for="email">Email *</label>
                  <input
                    type="email"
                    id="email"
                    v-model="formData.email"
                    required
                    placeholder="tu@email.com"
                  >
                </div>

                <div class="form-group">
                  <label for="telefono">Teléfono *</label>
                  <input
                    type="tel"
                    id="telefono"
                    v-model="formData.telefono"
                    required
                    placeholder="+57 300 123 4567"
                  >
                </div>

                <div class="form-group">
                  <label for="direccion">Dirección de envío *</label>
                  <textarea
                    id="direccion"
                    v-model="formData.direccion"
                    required
                    placeholder="Calle, número, ciudad, departamento"
                    rows="3"
                  ></textarea>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label for="ciudad">Ciudad *</label>
                    <input
                      type="text"
                      id="ciudad"
                      v-model="formData.ciudad"
                      required
                      placeholder="Ciudad"
                    >
                  </div>

                  <div class="form-group">
                    <label for="departamento">Departamento *</label>
                    <input
                      type="text"
                      id="departamento"
                      v-model="formData.departamento"
                      required
                      placeholder="Departamento"
                    >
                  </div>
                </div>

                <div class="form-section">
                  <h2>💳 Método de Pago</h2>
                  <div class="payment-methods">
                    <label class="payment-method">
                      <input
                        type="radio"
                        v-model="formData.metodoPago"
                        value="tarjeta"
                        required
                      >
                      <span class="payment-icon">💳</span>
                      <span class="payment-text">Tarjeta de Crédito/Débito</span>
                    </label>

                    <label class="payment-method">
                      <input
                        type="radio"
                        v-model="formData.metodoPago"
                        value="transferencia"
                        required
                      >
                      <span class="payment-icon">🏦</span>
                      <span class="payment-text">Transferencia Bancaria</span>
                    </label>

                    <label class="payment-method">
                      <input
                        type="radio"
                        v-model="formData.metodoPago"
                        value="contraentrega"
                        required
                      >
                      <span class="payment-icon">📦</span>
                      <span class="payment-text">Pago Contra Entrega</span>
                    </label>
                  </div>
                </div>

                <!-- Información de tarjeta (condicional) -->
                <div v-if="formData.metodoPago === 'tarjeta'" class="card-info">
                  <div class="form-group">
                    <label for="numeroTarjeta">Número de tarjeta *</label>
                    <input
                      type="text"
                      id="numeroTarjeta"
                      v-model="formData.numeroTarjeta"
                      placeholder="1234 5678 9012 3456"
                      maxlength="19"
                    >
                  </div>

                  <div class="form-row">
                    <div class="form-group">
                      <label for="fechaExpiracion">Fecha expiración *</label>
                      <input
                        type="text"
                        id="fechaExpiracion"
                        v-model="formData.fechaExpiracion"
                        placeholder="MM/AA"
                        maxlength="5"
                      >
                    </div>

                    <div class="form-group">
                      <label for="cvv">CVV *</label>
                      <input
                        type="text"
                        id="cvv"
                        v-model="formData.cvv"
                        placeholder="123"
                        maxlength="3"
                      >
                    </div>
                  </div>
                </div>

                <div class="form-actions">
                  <button
                    type="submit"
                    :disabled="processingCheckout || isEmpty"
                    class="btn-checkout"
                  >
                    <span v-if="processingCheckout" class="loading-spinner"></span>
                    <span v-else>✅ Confirmar Pedido</span>
                    <span class="total-amount">${{ formatPrice(totalAmount) }}</span>
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Resumen del pedido -->
          <div class="checkout-summary-section">
            <div class="summary-card">
              <h3>📋 Resumen del Pedido</h3>
              
              <div class="order-items">
                <div
                  v-for="item in cartItems"
                  :key="item.id"
                  class="order-item"
                >
                  <img :src="item.producto_imagen" :alt="item.producto_nombre" class="item-image">
                  <div class="item-details">
                    <h4>{{ item.producto_nombre }}</h4>
                    <p class="item-price">${{ formatPrice(item.producto_precio) }} c/u</p>
                    <p class="item-quantity">Cantidad: {{ item.cantidad }}</p>
                  </div>
                  <div class="item-subtotal">
                    ${{ formatPrice(item.subtotal) }}
                  </div>
                </div>
              </div>

              <div class="summary-totals">
                <div class="summary-row">
                  <span>Subtotal ({{ itemCount }} items):</span>
                  <span>${{ formatPrice(cartStore.cartTotal) }}</span>
                </div>
                
                <div class="summary-row">
                  <span>Envío:</span>
                  <span v-if="parseFloat(cartStore.cartTotal) > 50000" class="free-shipping">
                    GRATIS
                  </span>
                  <span v-else>$5.000</span>
                </div>

                <div class="summary-divider"></div>

                <div class="summary-row total">
                  <span><strong>Total:</strong></span>
                  <span class="total-amount">${{ formatPrice(totalAmount) }}</span>
                </div>

                <div v-if="parseFloat(cartStore.cartTotal) <= 50000" class="shipping-savings">
                  <span class="savings-icon">💸</span>
                  Agrega ${{ formatPrice(50000 - parseFloat(cartStore.cartTotal)) }} más para envío gratis
                </div>
              </div>
            </div>

            <!-- Garantías -->
            <div class="guarantees">
              <div class="guarantee-item">
                <span class="guarantee-icon">🛡️</span>
                <div class="guarantee-text">
                  <strong>Compra Segura</strong>
                  <span>Datos protegidos</span>
                </div>
              </div>
              <div class="guarantee-item">
                <span class="guarantee-icon">🚚</span>
                <div class="guarantee-text">
                  <strong>Envío Rápido</strong>
                  <span>24-48 horas</span>
                </div>
              </div>
              <div class="guarantee-item">
                <span class="guarantee-icon">↩️</span>
                <div class="guarantee-text">
                  <strong>Devoluciones</strong>
                  <span>30 días garantizados</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Carrito vacío -->
      <div v-else class="empty-checkout">
        <div class="empty-icon">🛒</div>
        <h2>Tu carrito está vacío</h2>
        <p>Agrega algunos productos antes de finalizar tu compra</p>
        <router-link to="/products" class="btn btn-primary">
          Explorar Productos
        </router-link>
      </div>

      <!-- Notificaciones -->
      <div v-if="showSuccess" class="success-modal">
        <div class="success-content">
          <div class="success-icon">🎉</div>
          <h2>¡Pedido Confirmado!</h2>
          <p>Tu pedido ha sido procesado exitosamente.</p>
          <p class="order-number">Número de pedido: #{{ orderNumber }}</p>
          <div class="success-actions">
            <router-link to="/products" class="btn btn-secondary">
              Seguir Comprando
            </router-link>
            <router-link to="/orders" class="btn btn-primary">
              Ver Mis Pedidos
            </router-link>
          </div>
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

export default {
  name: 'CheckoutView',
  setup() {
    const cartStore = useCartStore()
    const authStore = useAuthStore()
    const router = useRouter()

    const processingCheckout = ref(false)
    const showSuccess = ref(false)
    const orderNumber = ref('')

    // Datos del formulario
    const formData = ref({
      nombre: '',
      email: '',
      telefono: '',
      direccion: '',
      ciudad: '',
      departamento: '',
      metodoPago: 'tarjeta',
      numeroTarjeta: '',
      fechaExpiracion: '',
      cvv: ''
    })

    // Computed properties
    const cartItems = computed(() => cartStore.cartItems || [])
    const isEmpty = computed(() => cartStore.isEmpty)
    const itemCount = computed(() => cartStore.itemCount)

    const totalAmount = computed(() => {
      const subtotal = parseFloat(cartStore.cartTotal || 0)
      const shipping = subtotal > 50000 ? 0 : 5000
      return subtotal + shipping
    })

    // Métodos
    const formatPrice = (price) => {
      const number = parseFloat(price)
      return isNaN(number) ? '0' : number.toLocaleString('es-ES')
    }

    const processCheckout = async () => {
      processingCheckout.value = true

      try {
        // Validar formulario
        if (!validateForm()) {
          return
        }

        // Simular procesamiento del pago
        await new Promise(resolve => setTimeout(resolve, 2000))

        // Generar número de pedido
        orderNumber.value = 'ORD-' + Date.now().toString().slice(-6)

        // Mostrar éxito
        showSuccess.value = true

        // Limpiar carrito después de 3 segundos
        setTimeout(() => {
          cartStore.clearCart()
        }, 3000)

      } catch (error) {
        console.error('Error en checkout:', error)
        alert('Error procesando el pedido: ' + error.message)
      } finally {
        processingCheckout.value = false
      }
    }

    const validateForm = () => {
      const required = ['nombre', 'email', 'telefono', 'direccion', 'ciudad', 'departamento']
      
      for (const field of required) {
        if (!formData.value[field]?.trim()) {
          alert(`Por favor completa el campo: ${field}`)
          return false
        }
      }

      // Validaciones específicas para tarjeta
      if (formData.value.metodoPago === 'tarjeta') {
        if (!formData.value.numeroTarjeta?.trim() || 
            !formData.value.fechaExpiracion?.trim() || 
            !formData.value.cvv?.trim()) {
          alert('Por favor completa toda la información de la tarjeta')
          return false
        }
      }

      return true
    }

    // Verificar autenticación al cargar
    onMounted(() => {
      if (!authStore.isAuthenticated) {
        router.push('/login?redirect=checkout')
        return
      }

      if (cartStore.isEmpty) {
        router.push('/cart')
        return
      }

      // Pre-cargar datos del usuario si están disponibles
      if (authStore.user) {
        formData.value.nombre = authStore.user.nombre || ''
        formData.value.email = authStore.user.email || ''
      }
    })

    return {
      cartStore,
      cartItems,
      isEmpty,
      itemCount,
      totalAmount,
      processingCheckout,
      showSuccess,
      orderNumber,
      formData,
      processCheckout,
      formatPrice
    }
  }
}
</script>

<style scoped>
.checkout-view {
  padding: 2rem 0;
  background: #f8f9fa;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.checkout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.checkout-header h1 {
  color: #2c3e50;
  margin: 0;
  font-size: 2rem;
}

.back-to-cart {
  color: #6c757d;
  text-decoration: none;
  font-weight: 500;
}

.back-to-cart:hover {
  color: #495057;
}

.checkout-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: start;
}

/* Formulario */
.checkout-form-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 2rem;
}

.form-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #495057;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #27ae60;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

/* Métodos de pago */
.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.payment-method {
  display: flex;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.payment-method:hover {
  border-color: #27ae60;
}

.payment-method input[type="radio"] {
  margin-right: 1rem;
}

.payment-icon {
  font-size: 1.5rem;
  margin-right: 0.75rem;
}

.payment-text {
  font-weight: 500;
}

/* Información de tarjeta */
.card-info {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

/* Botón de checkout */
.btn-checkout {
  width: 100%;
  background: linear-gradient(135deg, #27ae60, #219a52);
  color: white;
  border: none;
  padding: 1.25rem 2rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-checkout:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
}

.btn-checkout:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Resumen */
.checkout-summary-section {
  position: sticky;
  top: 2rem;
}

.summary-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.summary-card h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.order-items {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
}

.order-item {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
}

.item-details {
  flex: 1;
}

.item-details h4 {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  color: #2c3e50;
}

.item-price, .item-quantity {
  margin: 0;
  font-size: 0.8rem;
  color: #6c757d;
}

.item-subtotal {
  font-weight: 600;
  color: #27ae60;
}

.summary-totals {
  border-top: 2px solid #e9ecef;
  padding-top: 1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  color: #495057;
}

.summary-row.total {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
}

.total-amount {
  color: #27ae60;
  font-weight: 700;
}

.summary-divider {
  height: 1px;
  background: #e9ecef;
  margin: 1rem 0;
}

.free-shipping {
  color: #27ae60;
  font-weight: 600;
}

.shipping-savings {
  background: #e8f5e8;
  border: 1px solid #27ae60;
  border-radius: 8px;
  padding: 0.75rem;
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #27ae60;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Garantías */
.guarantees {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.guarantee-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
}

.guarantee-item:not(:last-child) {
  border-bottom: 1px solid #e9ecef;
}

.guarantee-icon {
  font-size: 1.5rem;
}

.guarantee-text {
  display: flex;
  flex-direction: column;
}

.guarantee-text strong {
  color: #2c3e50;
  font-size: 0.9rem;
}

.guarantee-text span {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Estados vacío y éxito */
.empty-checkout {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.7;
}

.empty-checkout h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.empty-checkout p {
  color: #6c757d;
  margin-bottom: 2rem;
}

.success-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.success-content {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  max-width: 500px;
  width: 90%;
}

.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.success-content h2 {
  color: #27ae60;
  margin-bottom: 1rem;
}

.success-content p {
  color: #6c757d;
  margin-bottom: 1rem;
}

.order-number {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}

.success-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

/* Botones generales */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
}

.btn-primary {
  background: #27ae60;
  color: white;
}

.btn-primary:hover {
  background: #219a52;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Responsive */
@media (max-width: 968px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
  
  .checkout-summary-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .checkout-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .success-actions {
    flex-direction: column;
  }
  
  .btn-checkout {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}
</style>