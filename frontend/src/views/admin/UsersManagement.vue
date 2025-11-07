<template>
  <div class="users-management">
    <div class="page-header">
      <h2>Gestión de Usuarios</h2>
    </div>

    <!-- Filtros -->
    <div class="filters">
      <select v-model="filters.rol" @change="loadUsers" class="form-control">
        <option value="">Todos los roles</option>
        <option value="administrador">Administradores</option>
        <option value="cliente">Clientes</option>
      </select>
      
      <select v-model="filters.estado" @change="loadUsers" class="form-control">
        <option value="">Todos los estados</option>
        <option value="active">Activos</option>
        <option value="inactive">Inactivos</option>
      </select>
      
      <input
        v-model="filters.search"
        type="text"
        placeholder="Buscar usuarios..."
        class="form-control"
        @input="loadUsers"
      >
    </div>

    <!-- Estadísticas -->
    <div class="users-stats">
      <div class="stat-card">
        <div class="stat-number">{{ totalUsers }}</div>
        <div class="stat-label">Total Usuarios</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ clientsCount }}</div>
        <div class="stat-label">Clientes</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ adminsCount }}</div>
        <div class="stat-label">Administradores</div>
      </div>
    </div>

    <!-- Tabla de Usuarios -->
    <div class="table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>Usuario</th>
            <th>Email</th>
            <th>Teléfono</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Fecha Registro</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>
              <div class="user-info">
                <strong>{{ user.nombre || 'Sin nombre' }}</strong>
              </div>
            </td>
            <td>{{ user.email }}</td>
            <td>{{ user.telefono || 'No especificado' }}</td>
            <td>
              <span class="role-badge" :class="user.rol">
                {{ user.rol }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="user.activo ? 'active' : 'inactive'">
                {{ user.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td>{{ formatDate(user.fecha_creacion) }}</td>
            <td>
              <div class="action-buttons">
                <button 
                  @click="toggleUserStatus(user)"
                  class="btn btn-small"
                  :class="user.activo ? 'btn-warning' : 'btn-success'"
                  :title="user.activo ? 'Desactivar usuario' : 'Activar usuario'"
                >
                  {{ user.activo ? '❌' : '✅' }}
                </button>
                
                <button 
                  v-if="user.rol === 'cliente'"
                  @click="viewUserOrders(user)"
                  class="btn btn-small btn-secondary"
                  title="Ver pedidos"
                >
                  🛒
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Pedidos del Usuario -->
    <div v-if="selectedUser" class="modal-overlay">
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>Pedidos de {{ selectedUser.nombre }}</h3>
          <button @click="selectedUser = null" class="close-btn">×</button>
        </div>
        
        <div class="user-orders">
          <div v-if="userOrders.length === 0" class="no-orders">
            <p>Este usuario no ha realizado pedidos.</p>
          </div>
          
          <div v-else class="orders-list">
            <div v-for="order in userOrders" :key="order.id" class="order-card">
              <div class="order-header">
                <div class="order-info">
                  <strong>Pedido #{{ order.id }}</strong>
                  <span class="order-date">{{ formatDate(order.fecha_venta) }}</span>
                </div>
                <div class="order-status">
                  <span class="status-badge" :class="order.estado">{{ order.estado }}</span>
                  <span class="order-total">${{ order.total.toLocaleString() }}</span>
                </div>
              </div>
              
              <div class="order-products">
                <div v-for="detail in order.detalles" :key="detail.id" class="order-product">
                  <span class="product-name">{{ detail.producto_nombre }}</span>
                  <span class="product-quantity">x{{ detail.cantidad }}</span>
                  <span class="product-price">${{ detail.precio_unitario.toLocaleString() }}</span>
                </div>
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
import { saleService } from '../../services/saleService'
import dayjs from 'dayjs'

export default {
  name: 'UsersManagement',
  setup() {
    const users = ref([])
    const loading = ref(false)
    const selectedUser = ref(null)
    const userOrders = ref([])

    const filters = reactive({
      rol: '',
      estado: '',
      search: ''
    })

    const totalUsers = computed(() => users.value.length)
    const clientsCount = computed(() => users.value.filter(u => u.rol === 'cliente').length)
    const adminsCount = computed(() => users.value.filter(u => u.rol === 'administrador').length)

    const loadUsers = async () => {
      loading.value = true
      try {
        const data = await adminService.getAllUsers()
        
        let filteredUsers = data.users
        
        // Aplicar filtros
        if (filters.rol) {
          filteredUsers = filteredUsers.filter(user => user.rol === filters.rol)
        }
        
        if (filters.estado) {
          const isActive = filters.estado === 'active'
          filteredUsers = filteredUsers.filter(user => user.activo === isActive)
        }
        
        if (filters.search) {
          const searchLower = filters.search.toLowerCase()
          filteredUsers = filteredUsers.filter(user => 
            user.nombre?.toLowerCase().includes(searchLower) ||
            user.email.toLowerCase().includes(searchLower)
          )
        }
        
        users.value = filteredUsers
      } catch (error) {
        console.error('Error loading users:', error)
      } finally {
        loading.value = false
      }
    }

    const toggleUserStatus = async (user) => {
      const action = user.activo ? 'desactivar' : 'activar'
      const confirmMessage = `¿Estás seguro de que quieres ${action} a ${user.nombre || user.email}?`
      
      if (confirm(confirmMessage)) {
        try {
          // En una implementación real, aquí llamaríamos a la API para cambiar el estado
          // Por ahora, solo actualizamos localmente
          user.activo = !user.activo
          alert(`Usuario ${action}do exitosamente!`)
        } catch (error) {
          alert('Error actualizando usuario')
        }
      }
    }

    const viewUserOrders = async (user) => {
      selectedUser.value = user
      try {
        // En una implementación real, el admin podría ver los pedidos de cualquier usuario
        // Por ahora, simulamos cargando algunos datos
        userOrders.value = [] // Se cargarían los pedidos reales del usuario
      } catch (error) {
        console.error('Error loading user orders:', error)
      }
    }

    const formatDate = (dateString) => {
      return dayjs(dateString).format('DD/MM/YYYY')
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users,
      filters,
      selectedUser,
      userOrders,
      totalUsers,
      clientsCount,
      adminsCount,
      loadUsers,
      toggleUserStatus,
      viewUserOrders,
      formatDate
    }
  }
}
</script>

<style scoped>
.users-management {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.users-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.stat-card {
  background: var(--white);
  padding: 20px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-green);
  margin-bottom: 5px;
}

.stat-label {
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.table-container {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid var(--medium-gray);
}

.users-table th {
  background: var(--light-gray);
  font-weight: 600;
  color: var(--text-dark);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.role-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.role-badge.administrador {
  background: var(--primary-green);
  color: var(--white);
}

.role-badge.cliente {
  background: var(--light-gray);
  color: var(--text-dark);
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-badge.active {
  background: var(--success);
  color: var(--white);
}

.status-badge.inactive {
  background: var(--dark-gray);
  color: var(--white);
}

.status-badge.pendiente {
  background: #fff3cd;
  color: #856404;
}

.status-badge.completado {
  background: var(--success);
  color: var(--white);
}

.action-buttons {
  display: flex;
  gap: 5px;
}

.btn-small {
  padding: 6px 10px;
  font-size: 0.8rem;
}

.btn-warning {
  background: var(--warning);
  color: var(--text-dark);
}

.btn-success {
  background: var(--success);
  color: var(--white);
}

.user-orders {
  max-height: 60vh;
  overflow-y: auto;
}

.no-orders {
  text-align: center;
  padding: 40px;
  color: var(--dark-gray);
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.order-card {
  background: var(--light-gray);
  padding: 15px;
  border-radius: var(--border-radius);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.order-date {
  font-size: 0.8rem;
  color: var(--dark-gray);
}

.order-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.order-total {
  font-weight: bold;
  color: var(--primary-green);
}

.order-products {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.order-product {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  background: var(--white);
  border-radius: 4px;
}

.product-name {
  flex: 1;
}

.product-quantity {
  color: var(--dark-gray);
  margin: 0 10px;
}

.product-price {
  font-weight: 500;
  color: var(--primary-green);
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .users-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .order-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .order-status {
    width: 100%;
    justify-content: space-between;
  }
}
</style>