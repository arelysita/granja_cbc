<template>
  <div class="dashboard">
    <!-- Estadísticas Rápidas -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📦</div>
        <div class="stat-info">
          <h3>{{ stats.total_products }}</h3>
          <p>Productos Totales</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-info">
          <h3>${{ stats.monthly_revenue?.toLocaleString() || '0' }}</h3>
          <p>Ingresos del Mes</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <h3>{{ stats.total_users }}</h3>
          <p>Usuarios Registrados</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🛒</div>
        <div class="stat-info">
          <h3>{{ stats.monthly_sales }}</h3>
          <p>Ventas del Mes</p>
        </div>
      </div>
    </div>

    <!-- Gráficos y Métricas -->
    <div class="charts-grid">
      <div class="chart-card">
        <h3>Ventas por Categoría</h3>
        <BarChart v-if="salesByCategory.length" :chart-data="salesByCategoryChartData" />
        <div v-else class="no-data">No hay datos disponibles</div>
      </div>
      
      <div class="chart-card">
        <h3>Métricas Clave</h3>
        <div class="metrics-list">
          <div class="metric-item">
            <span class="metric-label">Productos con Stock Bajo:</span>
            <span class="metric-value warning">{{ stats.low_stock_products }}</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Ventas Totales:</span>
            <span class="metric-value">{{ stats.total_sales }}</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">Categorías Activas:</span>
            <span class="metric-value">{{ stats.total_categories }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Ventas Recientes -->
    <div class="recent-sales">
      <h3>Ventas Recientes</h3>
      <div v-if="recentSales.length" class="sales-list">
        <div v-for="sale in recentSales" :key="sale.id" class="sale-item">
          <div class="sale-info">
            <strong>Venta #{{ sale.id }}</strong>
            <span class="sale-date">{{ formatDate(sale.fecha_venta) }}</span>
          </div>
          <div class="sale-details">
            <span class="sale-customer">{{ sale.cliente_nombre }}</span>
            <span class="sale-amount">${{ sale.total.toLocaleString() }}</span>
            <span class="sale-status" :class="sale.estado">{{ sale.estado }}</span>
          </div>
        </div>
      </div>
      <div v-else class="no-data">
        No hay ventas recientes
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { adminService } from '../../services/adminService'
import BarChart from '../../components/charts/BarChart.vue'
import dayjs from 'dayjs'

export default {
  name: 'DashboardView',
  components: {
    BarChart
  },
  setup() {
    const stats = ref({
      total_products: 0,
      monthly_revenue: 0,
      total_users: 0,
      monthly_sales: 0,
      total_sales: 0,
      total_categories: 0,
      low_stock_products: 0
    })
    
    const salesByCategory = ref([])
    const recentSales = ref([])
    const loading = ref(true)

    const salesByCategoryChartData = computed(() => {
      return {
        labels: salesByCategory.value.map(item => item.categoria),
        datasets: [{
          label: 'Ventas por Categoría',
          data: salesByCategory.value.map(item => item.total),
          backgroundColor: '#2E8B57',
          borderColor: '#2E8B57',
          borderWidth: 1
        }]
      }
    })

    const loadDashboardData = async () => {
      try {
        // Cargar estadísticas
        const statsData = await adminService.getDashboardStats()
        stats.value = statsData.stats

        // Cargar ventas por categoría
        const categoryData = await adminService.getSalesByCategory()
        salesByCategory.value = categoryData.sales_by_category

        // Cargar ventas recientes
        const salesData = await adminService.getAllSales({ per_page: 5 })
        recentSales.value = salesData.sales

      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      return dayjs(dateString).format('DD/MM/YYYY HH:mm')
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      stats,
      salesByCategory,
      recentSales,
      loading,
      salesByCategoryChartData,
      formatDate
    }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: var(--white);
  padding: 25px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: var(--transition);
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-icon {
  font-size: 3rem;
}

.stat-info h3 {
  font-size: 2rem;
  margin: 0;
  color: var(--primary-green);
}

.stat-info p {
  margin: 5px 0 0;
  color: var(--dark-gray);
}

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart-card {
  background: var(--white);
  padding: 25px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.chart-card h3 {
  margin: 0 0 20px;
  color: var(--text-dark);
}

.metrics-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: var(--light-gray);
  border-radius: var(--border-radius);
}

.metric-label {
  font-weight: 500;
}

.metric-value {
  font-weight: bold;
  color: var(--primary-green);
}

.metric-value.warning {
  color: var(--warning);
}

.recent-sales {
  background: var(--white);
  padding: 25px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.recent-sales h3 {
  margin: 0 0 20px;
  color: var(--text-dark);
}

.sales-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.sale-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: var(--light-gray);
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.sale-item:hover {
  background: var(--medium-gray);
}

.sale-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.sale-date {
  font-size: 0.9rem;
  color: var(--dark-gray);
}

.sale-details {
  display: flex;
  align-items: center;
  gap: 15px;
}

.sale-customer {
  font-weight: 500;
}

.sale-amount {
  font-weight: bold;
  color: var(--primary-green);
}

.sale-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.sale-status.completado {
  background: var(--success);
  color: var(--white);
}

.sale-status.pendiente {
  background: var(--warning);
  color: var(--text-dark);
}

.sale-status.procesando {
  background: var(--primary-green);
  color: var(--white);
}

.no-data {
  text-align: center;
  padding: 40px;
  color: var(--dark-gray);
  font-style: italic;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .sale-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .sale-details {
    width: 100%;
    justify-content: space-between;
  }
}
</style>