// Archivo creado automáticamente
<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/" class="navbar-brand">
          Granja CBC
        </router-link>
        
        <div class="navbar-menu">
          <router-link to="/products" class="navbar-link">
            Productos
          </router-link>
          
          <template v-if="isAuthenticated">
            <router-link v-if="isClient" to="/cart" class="navbar-link cart-link">
              🛒 Carrito
              <span v-if="cartCount > 0" class="cart-count">{{ cartCount }}</span>
            </router-link>
            
            <router-link v-if="isClient" to="/orders" class="navbar-link">
              Mis Pedidos
            </router-link>
            
            <router-link v-if="isAdmin" to="/admin" class="navbar-link">
              Administración
            </router-link>
            
            <div class="navbar-user">
              <span>Hola, {{ userName }}</span>
              <div class="user-dropdown">
                <router-link to="/profile" class="dropdown-item">Perfil</router-link>
                <button @click="logout" class="dropdown-item">Cerrar Sesión</button>
              </div>
            </div>
          </template>
          
          <template v-else>
            <router-link to="/login" class="navbar-link">
              Iniciar Sesión
            </router-link>
            <router-link to="/register" class="btn btn-primary">
              Crear Cuenta
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../../store/auth'
import { useCartStore } from '../../store/cart'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Navbar',
  setup() {
    const authStore = useAuthStore()
    const cartStore = useCartStore()
    const router = useRouter()

    const logout = () => {
      authStore.logout()
      router.push('/')
    }

    return {
      isAuthenticated: computed(() => authStore.isAuthenticated),
      isAdmin: computed(() => authStore.isAdmin),
      isClient: computed(() => authStore.isClient),
      userName: computed(() => authStore.userName),
      cartCount: computed(() => cartStore.itemCount),
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  background: var(--white);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}

.navbar-brand {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-green);
  text-decoration: none;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.navbar-link {
  color: var(--text-dark);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.navbar-link:hover {
  background-color: var(--light-green);
}

.cart-link {
  position: relative;
}

.cart-count {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--danger);
  color: var(--white);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-user {
  position: relative;
  cursor: pointer;
  padding: 8px 16px;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  min-width: 150px;
  display: none;
}

.navbar-user:hover .user-dropdown {
  display: block;
}

.dropdown-item {
  display: block;
  padding: 10px 15px;
  color: var(--text-dark);
  text-decoration: none;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: var(--light-gray);
}
</style>