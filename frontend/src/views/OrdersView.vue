<template>
  <div class="orders-view">
    <div class="container">
      <!-- Header -->
      <div class="orders-header">
        <h1>📦 Mis Pedidos</h1>
        <p>Gestiona y revisa el estado de tus pedidos</p>
      </div>

      <!-- Sin órdenes -->
      <div v-if="isEmpty && !isLoading" class="empty-state">
        <div class="empty-icon">📦</div>
        <h3>No tienes pedidos aún</h3>
        <p>Cuando realices tu primer pedido, aparecerá aquí.</p>
        <div class="empty-actions">
          <router-link to="/products" class="btn btn-primary">
            Explorar Productos
          </router-link>
          <router-link to="/cart" class="btn btn-secondary">
            Ver Carrito
          </router-link>
        </div>
      </div>

      <!-- Lista de órdenes -->
      <div v-else class="orders-content">
        <div class="orders-stats">
          <div class="stat-item">
            <span class="stat-label">Total de pedidos:</span>
            <span class="stat-value">{{ orders.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Pedido más reciente:</span>
            <span class="stat-value">{{ latestOrderDate }}</span>
          </div>
        </div>

        <div class="orders-list">
          <div 
            v-for="order in orders" 
            :key="order.id" 
            class="order-card"
          >
            <div class="order-header">
              <div class="order-info">
                <h3 class="order-number">{{ order.order_number }}</h3>
                <p class="order-date">{{ formatDate(order.created_at) }}</p>
                <p class="order-address">
                  📍 {{ order.shipping_address }}
                </p>
              </div>
              <div class="order-status">
                <span :class="['status-badge', getStatusBadge(order.status).class]">
                  {{ getStatusBadge(order.status).text }}
                </span>
              </div>
            </div>

            <div class="order-items">
              <div 
                v-for="item in order.items" 
                :key="item.product_id" 
                class="order-item"
              >
                <img 
                  :src="item.image || '/placeholder-product.jpg'" 
                  :alt="item.product_name"
                  class="item-image"
                  @error="handleImageError"
                >
                <div class="item-details">
                  <h4>{{ item.product_name }}</h4>
                  <p class="item-meta">
                    Cantidad: {{ item.quantity }} • 
                    ${{ formatPrice(item.price) }} c/u
                  </p>
                </div>
                <div class="item-subtotal">
                  ${{ formatPrice(item.subtotal) }}
                </div>
              </div>
            </div>

            <div class="order-summary">
              <div class="summary-row">
                <span>Subtotal:</span>
                <span>${{ formatPrice(order.subtotal) }}</span>
              </div>
              <div class="summary-row">
                <span>Envío:</span>
                <span>{{ order.shipping_cost === 0 ? 'GRATIS' : `$${formatPrice(order.shipping_cost)}` }}</span>
              </div>
              <div class="summary-row total">
                <span><strong>Total:</strong></span>
                <span class="total-amount">${{ formatPrice(order.total) }}</span>
              </div>
            </div>

            <div class="order-footer">
              <div class="payment-info">
                <span class="payment-method">
                  💳 {{ getPaymentMethodText(order.payment_method) }}
                </span>
              </div>
              <div class="order-actions">
                <button 
                  @click="viewOrderDetails(order)" 
                  class="btn btn-outline"
                >
                  👁️ Ver Detalles
                </button>
                <button 
                  v-if="order.status === 'completed'" 
                  @click="downloadInvoice(order)"
                  class="btn btn-outline"
                >
                  📄 Descargar Factura
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useOrdersStore } from '../store/orders'

export default {
  name: 'OrdersView',
  setup() {
    const ordersStore = useOrdersStore()
    const isLoading = ref(false)

    // Cargar órdenes al montar el componente
    onMounted(() => {
      loadOrders()
    })

    const loadOrders = () => {
      isLoading.value = true
      try {
        ordersStore.fetchOrders()
        console.log('✅ Órdenes cargadas:', ordersStore.orders.length)
      } catch (error) {
        console.error('❌ Error cargando órdenes:', error)
      } finally {
        isLoading.value = false
      }
    }

    const orders = computed(() => ordersStore.sortedOrders)
    const isEmpty = computed(() => ordersStore.isEmpty)

    const latestOrderDate = computed(() => {
      if (orders.value.length === 0) return 'N/A'
      return formatDate(orders.value[0].created_at)
    })

    const formatPrice = (price) => {
      const number = parseFloat(price)
      return isNaN(number) ? '0' : number.toLocaleString('es-ES')
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Fecha no disponible'
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getStatusBadge = (status) => {
      const statusMap = {
        pending: { class: 'status-pending', text: 'Pendiente' },
        completed: { class: 'status-completed', text: 'Completado' },
        cancelled: { class: 'status-cancelled', text: 'Cancelado' },
        shipping: { class: 'status-shipping', text: 'En envío' },
        processing: { class: 'status-processing', text: 'Procesando' }
      }
      return statusMap[status] || { class: 'status-pending', text: status || 'Pendiente' }
    }

    const getPaymentMethodText = (method) => {
      const methods = {
        tarjeta: 'Tarjeta de Crédito/Débito',
        transferencia: 'Transferencia Bancaria',
        contraentrega: 'Pago Contra Entrega'
      }
      return methods[method] || method
    }

    const handleImageError = (event) => {
      event.target.src = '/placeholder-product.jpg'
    }

    const viewOrderDetails = (order) => {
      const details = `
Pedido: ${order.order_number}
Fecha: ${formatDate(order.created_at)}
Estado: ${getStatusBadge(order.status).text}
Total: $${formatPrice(order.total)}
Método de pago: ${getPaymentMethodText(order.payment_method)}
Dirección: ${order.shipping_address}

Productos:
${order.items.map(item => 
  `• ${item.product_name} - ${item.quantity} x $${formatPrice(item.price)} = $${formatPrice(item.subtotal)}`
).join('\n')}
      `
      alert(details)
    }

    const downloadInvoice = (order) => {
      // Simular descarga de factura
      const invoiceContent = `
FACTURA - ${order.order_number}
Fecha: ${formatDate(order.created_at)}
Cliente: ${order.customer_name}
Email: ${order.customer_email}
Teléfono: ${order.customer_phone}

DETALLES DEL PEDIDO:
${order.items.map(item => 
  `${item.product_name} - ${item.quantity} x $${formatPrice(item.price)} = $${formatPrice(item.subtotal)}`
).join('\n')}

SUBTOTAL: $${formatPrice(order.subtotal)}
ENVÍO: ${order.shipping_cost === 0 ? 'GRATIS' : `$${formatPrice(order.shipping_cost)}`}
TOTAL: $${formatPrice(order.total)}

Método de pago: ${getPaymentMethodText(order.payment_method)}
Dirección de envío: ${order.shipping_address}

¡Gracias por tu compra!
      `
      
      const blob = new Blob([invoiceContent], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `factura-${order.order_number}.txt`
      a.click()
      URL.revokeObjectURL(url)
      
      alert(`📄 Factura ${order.order_number} descargada`)
    }

    return {
      orders,
      isLoading,
      isEmpty,
      latestOrderDate,
      loadOrders,
      formatPrice,
      formatDate,
      getStatusBadge,
      getPaymentMethodText,
      handleImageError,
      viewOrderDetails,
      downloadInvoice
    }
  }
}
</script>

<style scoped>
.orders-view {
  padding: 2rem 0;
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1rem;
}

.orders-header {
  text-align: center;
  margin-bottom: 2rem;
}

.orders-header h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
}

.orders-header p {
  color: #6c757d;
  font-size: 1.2rem;
}

/* Estados */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  opacity: 0.6;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.empty-state p {
  color: #6c757d;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.empty-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Estadísticas */
.orders-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-item {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #6c757d;
  font-weight: 500;
}

.stat-value {
  color: #2c3e50;
  font-weight: 700;
  font-size: 1.1rem;
}

/* Lista de órdenes */
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.order-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.order-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #e9ecef;
}

.order-info {
  flex: 1;
}

.order-number {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
  font-size: 1.4rem;
  font-weight: 700;
}

.order-date {
  margin: 0 0 0.5rem 0;
  color: #6c757d;
  font-size: 1rem;
}

.order-address {
  margin: 0;
  color: #495057;
  font-size: 0.9rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.status-completed {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #b8daff;
}

.status-cancelled {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-shipping {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-processing {
  background: #cce7ff;
  color: #004085;
  border: 1px solid #b3d7ff;
}

/* Items de la orden */
.order-items {
  margin-bottom: 1.5rem;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.item-details {
  flex: 1;
}

.item-details h4 {
  margin: 0 0 0.25rem 0;
  color: #2c3e50;
  font-size: 1rem;
}

.item-meta {
  margin: 0;
  color: #6c757d;
  font-size: 0.85rem;
}

.item-subtotal {
  font-weight: 700;
  color: #27ae60;
  font-size: 1.1rem;
}

/* Resumen */
.order-summary {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  color: #495057;
}

.summary-row:last-child {
  margin-bottom: 0;
}

.summary-row.total {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
  border-top: 2px solid #dee2e6;
  padding-top: 0.75rem;
  margin-top: 0.75rem;
}

.total-amount {
  color: #27ae60;
}

/* Footer de la orden */
.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.5rem;
  border-top: 2px solid #e9ecef;
}

.payment-method {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.order-actions {
  display: flex;
  gap: 0.75rem;
}

/* Botones */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.btn-primary {
  background: #27ae60;
  color: white;
}

.btn-primary:hover {
  background: #219a52;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  color: #495057;
  border: 2px solid #dee2e6;
}

.btn-outline:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
  transform: translateY(-1px);
}

/* Responsive */
@media (max-width: 768px) {
  .order-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .order-footer {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .order-actions {
    justify-content: center;
  }
  
  .order-item {
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }
  
  .item-image {
    align-self: center;
  }
  
  .orders-stats {
    grid-template-columns: 1fr;
  }
  
  .empty-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>