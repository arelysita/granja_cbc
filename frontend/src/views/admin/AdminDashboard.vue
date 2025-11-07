<template>
  <div class="admin-dashboard">
    <div class="admin-sidebar">
      <div class="sidebar-header">
        <h2>🌱 Admin CBC</h2>
      </div>
      
      <nav class="sidebar-nav">
        <router-link 
          to="/admin/dashboard" 
          class="nav-item"
          :class="{ active: $route.name === 'AdminDashboard' }"
        >
          📊 Dashboard
        </router-link>
        
        <router-link 
          to="/admin/products" 
          class="nav-item"
          :class="{ active: $route.name === 'AdminProducts' }"
        >
          📦 Productos
        </router-link>
        
        <router-link 
          to="/admin/sales" 
          class="nav-item"
          :class="{ active: $route.name === 'AdminSales' }"
        >
          💰 Ventas
        </router-link>
        
        <router-link 
          to="/admin/users" 
          class="nav-item"
          :class="{ active: $route.name === 'AdminUsers' }"
        >
          👥 Usuarios
        </router-link>
        
        <router-link 
          to="/admin/reviews" 
          class="nav-item"
          :class="{ active: $route.name === 'AdminReviews' }"
        >
          ⭐ Reseñas
        </router-link>
      </nav>
      
      <div class="sidebar-footer">
        <router-link to="/" class="nav-item">
          🏠 Volver al Sitio
        </router-link>
        <button @click="authStore.logout()" class="nav-item logout-btn">
          🚪 Cerrar Sesión
        </button>
      </div>
    </div>
    
    <div class="admin-content">
      <header class="admin-header">
        <h1>{{ pageTitle }}</h1>
        <div class="admin-user">
          <span>Hola, {{ authStore.userName }}</span>
        </div>
      </header>
      
      <main class="admin-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'AdminDashboard',
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()

    const pageTitle = computed(() => {
      const titles = {
        'AdminDashboard': 'Dashboard',
        'AdminProducts': 'Gestión de Productos',
        'AdminSales': 'Gestión de Ventas',
        'AdminUsers': 'Gestión de Usuarios',
        'AdminReviews': 'Moderación de Reseñas'
      }
      return titles[route.name] || 'Administración'
    })

    return {
      authStore,
      pageTitle
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
}

.admin-sidebar {
  width: 280px;
  background: var(--dark-green);
  color: var(--white);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 30px 25px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  margin: 0;
  color: var(--light-green);
}

.sidebar-nav {
  flex: 1;
  padding: 20px 0;
}

.nav-item {
  display: block;
  padding: 15px 25px;
  color: var(--white);
  text-decoration: none;
  transition: var(--transition);
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 1rem;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.nav-item.active {
  background: var(--primary-green);
  border-right: 4px solid var(--light-green);
}

.sidebar-footer {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px 0;
}

.logout-btn {
  color: #ff6b6b;
}

.logout-btn:hover {
  background: rgba(255, 107, 107, 0.1);
}

.admin-content {
  flex: 1;
  background: var(--light-gray);
  display: flex;
  flex-direction: column;
}

.admin-header {
  background: var(--white);
  padding: 20px 30px;
  box-shadow: var(--box-shadow);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.admin-header h1 {
  margin: 0;
  color: var(--primary-green);
  font-size: 1.8rem;
}

.admin-user {
  color: var(--dark-gray);
  font-weight: 500;
}

.admin-main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .admin-dashboard {
    flex-direction: column;
  }
  
  .admin-sidebar {
    width: 100%;
    height: auto;
  }
  
  .sidebar-nav {
    display: flex;
    overflow-x: auto;
    padding: 10px 0;
  }
  
  .nav-item {
    white-space: nowrap;
    padding: 10px 15px;
  }
}
</style>