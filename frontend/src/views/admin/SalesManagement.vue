<template>
  <div class="sales-management">
    <div class="page-header">
      <h2>Gestión de Ventas</h2>
    </div>

    <!-- Filtros -->
    <div class="filters">
      <select v-model="filters.estado" @change="loadSales" class="form-control">
        <option value="">Todos los estados</option>
        <option value="pendiente">Pendiente</option>
        <option value="procesando">Procesando</option>
        <option value="enviado">Enviado</option>
        <option value="completado">Completado</option>
        <option value="cancelado">Cancelado</option>
      </select>
      
      <input
        v-model="filters.search"
        type="text"
        placeholder="Buscar por cliente..."
        class="form-control"
        @input="loadSales"
      >
    </div>

    <!-- Estadísticas Rápidas -->
    <div class="sales-stats">
      <div class="stat-item">
        <span class="stat-label">Total Ventas:</span>
        <span class="stat-value">{{ sales.length }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Ingresos Totales:</span>
        <span class="stat-value">${{ totalRevenue.toLocaleString() }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">Ventas Pendientes:</span>
        <span class="stat-value">{{ pendingSalesCount }}</span>
      </div>
    </div>

    <!-- Tabla de Ventas -->
    <div class="table-container">
      <table class="sales-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Fecha</th>
            <th>Total</th>
            <th>Método Pago</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sale in sales" :key="sale.id">
            <td>#{{ sale.id }}</td>
            <td>
              <strong>{{ sale.cliente_nombre }}</strong>
              <div class="customer-email">{{ getCustomerEmail(sale.cliente_id) }}</div>
            </td>
            <td>{{ formatDate(sale.fecha_venta) }}</td>
            <td>${{ sale.total.toLocaleString() }}</td>
            <td>
              <span class="payment-method">{{ formatPaymentMethod(sale.metodo_pago) }}</span>
            </td>
            <td>
              <select 
                v-model="sale.estado" 
                @change="updateSaleStatus(sale)"
                class="status-select"
                :class="sale.estado"
              >
                <option value="pendiente">Pendiente</option>
                <option value="procesando">Procesando</option>
                <option value="enviado">Enviado</option>
                <option value="completado">Completado</option>
                <option value="cancelado">Cancelado</option>
              </select>
            </td>
            <td>
              <div class="action-buttons">
                <button 
                  @click="viewSaleDetails(sale)"
                  class="btn btn-small btn-secondary"
                  title="Ver detalles"
                >
                  👁️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Paginación -->
    <div v-if="pagination.pages > 1" class="pagination">
      <button 
        @click="changePage(pagination.current_page - 1)"
        :disabled="pagination.current_page === 1"
        class="btn btn-secondary"
      >
        Anterior
      </button>
      <span>Página {{ pagination.current_page }} de {{ pagination.pages }}</span>
      <button 
        @click="changePage(pagination.current_page + 1)"
        :disabled="pagination.current_page === pagination.pages"
        class="btn btn-secondary"
      >
        Siguiente
      </button>
    </div>

    <!-- Modal Detalles de Venta -->
    <div v-if="selectedSale" class="modal-overlay">
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>Detalles de Venta #{{ selectedSale.id }}</h3>
          <button @click="selectedSale = null" class="close-btn">×</button>
        </div>
        
        <div class="sale-details">
          <!-- Información del Cliente -->
          <div class="detail-section">
            <h4>Información del Cliente</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <strong>Nombre:</strong>
                <span>{{ selectedSale.cliente_nombre }}</span>
              </div>
              <div class="detail-item">
                <strong>Dirección:</strong>
                <span>{{ selectedSale.direccion_envio || 'No especificada' }}</span>
              </div>
              <div class="detail-item">
                <strong>Método de Pago:</strong>
                <span>{{ formatPaymentMethod(selectedSale.metodo_pago) }}</span>
              </div>
            </div>
          </div>

          <!-- Productos -->
          <div class="detail-section">
            <h4>Productos</h4>
            <div class="products-list">
              <div v-for="detail in selectedSale.detalles" :key="detail.id" class="product-item">
                <img 
                  :src="getProductImage(detail.producto_id)" 
                  :alt="detail.producto_nombre"
                  class="product-thumb"
                >
                <div class="product-info">
                  <strong>{{ detail.producto_nombre }}</strong>
                  <div class="product-meta">
                    <span>Cantidad: {{ detail.cantidad }}</span>
                    <span>Precio: ${{ detail.precio_unitario.toLocaleString() }}</span>
                    <span>Subtotal: ${{ (detail.cantidad * detail.precio_unitario).toLocaleString() }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Resumen -->
          <div class="detail-section">
            <h4>Resumen</h4>
            <div class="summary">
              <div class="summary-row">
                <span>Subtotal:</span>
                <span>${{ selectedSale.total.toLocaleString() }}</span>
              </div>
              <div class="summary-row">
                <span>Envío:</span>
                <span>Gratis</span>
              </div>
              <div class="summary-row total">
                <span>Total:</span>
                <span>${{ selectedSale.total.toLocaleString() }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, reactive, computed } from 'vue'
import { adminService } from '../../services/adminService'
import { productService } from '../../services/productService'
import dayjs from 'dayjs'

export default {
  name: 'SalesManagement',
  setup() {
    const sales = ref([])
    const allUsers = ref([])
    const products = ref([])
    const loading = ref(false)
    const selectedSale = ref(null)

    const filters = reactive({
      estado: '',
      search: ''
    })

    const pagination = reactive({
      current_page: 1,
      pages: 1,
      total: 0
    })

    const totalRevenue = computed(() => {
      return sales.value.reduce((total, sale) => total + sale.total, 0)
    })

    const pendingSalesCount = computed(() => {
      return sales.value.filter(sale => sale.estado === 'pendiente').length
    })

    const loadSales = async (page = 1) => {
      loading.value = true
      try {
        const params = {
          page,
          per_page: 15
        }

        if (filters.estado) params.estado = filters.estado
        if (filters.search) params.search = filters.search

        const data = await adminService.getAllSales(params)
        sales.value = data.sales
        pagination.current_page = data.current_page
        pagination.pages = data.pages
        pagination.total = data.total
      } catch (error) {
        console.error('Error loading sales:', error)
      } finally {
        loading.value = false
      }
    }

    const loadUsers = async () => {
      try {
        const data = await adminService.getAllUsers()
        allUsers.value = data.users
      } catch (error) {
        console.error('Error loading users:', error)
      }
    }

    const updateSaleStatus = async (sale) => {
      try {
        await adminService.updateSaleStatus(sale.id, sale.estado)
        alert('Estado de venta actualizado exitosamente!')
      } catch (error) {
        alert('Error actualizando estado de venta')
        // Revertir el cambio en caso de error
        loadSales(pagination.current_page)
      }
    }

    const viewSaleDetails = (sale) => {
      selectedSale.value = sale
    }

    const getCustomerEmail = (clienteId) => {
      const user = allUsers.value.find(u => u.id === clienteId)
      return user ? user.email : 'N/A'
    }

    const getProductImage = (productoId) => {
      const product = products.value.find(p => p.id === productoId)
      return product?.imagen_url || '/placeholder-product.jpg'
    }

    const formatDate = (dateString) => {
      return dayjs(dateString).format('DD/MM/YYYY HH:mm')
    }

    const formatPaymentMethod = (method) => {
      const methods = {
        'contra_entrega': 'Contra Entrega',
        'tarjeta_credito': 'Tarjeta de Crédito',
        'tarjeta_debito': 'Tarjeta de Débito',
        'pse': 'PSE',
        'nequi': 'Nequi',
        'daviplata': 'Daviplata'
      }
      return methods[method] || method
    }

    const changePage = (page) => {
      if (page >= 1 && page <= pagination.pages) {
        loadSales(page)
      }
    }

    onMounted(() => {
      loadSales()
      loadUsers()
    })

    return {
      sales,
      filters,
      pagination,
      selectedSale,
      totalRevenue,
      pendingSalesCount,
      loadSales,
      updateSaleStatus,
      viewSaleDetails,
      getCustomerEmail,
      getProductImage,
      formatDate,
      formatPaymentMethod,
      changePage
    }
  }
}
</script>

<style scoped>
.sales-management {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.sales-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.stat-item {
  background: var(--white);
  padding: 20px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--dark-gray);
  margin-bottom: 5px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-green);
}

.table-container {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.sales-table {
  width: 100%;
  border-collapse: collapse;
}

.sales-table th,
.sales-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid var(--medium-gray);
}

.sales-table th {
  background: var(--light-gray);
  font-weight: 600;
  color: var(--text-dark);
}

.customer-email {
  font-size: 0.8rem;
  color: var(--dark-gray);
  margin-top: 5px;
}

.payment-method {
  padding: 4px 8px;
  background: var(--light-gray);
  border-radius: 12px;
  font-size: 0.8rem;
}

.status-select {
  padding: 6px 10px;
  border: 1px solid var(--medium-gray);
  border-radius: var(--border-radius);
  font-size: 0.9rem;
  cursor: pointer;
  transition: var(--transition);
}

.status-select.pendiente {
  background: #fff3cd;
  color: #856404;
}

.status-select.procesando {
  background: #d1ecf1;
  color: #0c5460;
}

.status-select.enviado {
  background: #d4edda;
  color: #155724;
}

.status-select.completado {
  background: var(--success);
  color: var(--white);
}

.status-select.cancelado {
  background: #f8d7da;
  color: #721c24;
}

.action-buttons {
  display: flex;
  gap: 5px;
}

.btn-small {
  padding: 6px 10px;
  font-size: 0.8rem;
}

.modal-large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--medium-gray);
}

.modal-header h3 {
  margin: 0;
  color: var(--primary-green);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--dark-gray);
}

.sale-details {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.detail-section h4 {
  margin: 0 0 15px;
  color: var(--text-dark);
  border-bottom: 2px solid var(--light-green);
  padding-bottom: 8px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-item strong {
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.product-item {
  display: flex;
  gap: 15px;
  padding: 15px;
  background: var(--light-gray);
  border-radius: var(--border-radius);
}

.product-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.product-info {
  flex: 1;
}

.product-meta {
  display: flex;
  gap: 15px;
  margin-top: 8px;
  font-size: 0.9rem;
  color: var(--dark-gray);
}

.summary {
  max-width: 300px;
  margin-left: auto;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--medium-gray);
}

.summary-row.total {
  border-top: 2px solid var(--medium-gray);
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--primary-green);
  margin-top: 10px;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .sales-stats {
    grid-template-columns: 1fr;
  }
  
  .product-meta {
    flex-direction: column;
    gap: 5px;
  }
  
  .summary {
    max-width: none;
  }
}
</style>