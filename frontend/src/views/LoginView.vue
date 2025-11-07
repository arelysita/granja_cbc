// Archivo creado automáticamente
<template>
  <div class="login">
    <div class="container">
      <div class="login-container">
        <div class="login-card">
          <h2>Iniciar Sesión</h2>
          <p class="login-subtitle">Accede a tu cuenta de Granja CBC</p>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label class="form-label">Email</label>
              <input
                v-model="form.email"
                type="email"
                class="form-control"
                placeholder="tu@email.com"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Contraseña</label>
              <input
                v-model="form.password"
                type="password"
                class="form-control"
                placeholder="Tu contraseña"
                required
              >
            </div>

            <div v-if="authStore.error" class="alert alert-error">
              {{ authStore.error }}
            </div>

            <button 
              type="submit" 
              class="btn btn-primary btn-block"
              :disabled="authStore.isLoading"
            >
              <span v-if="authStore.isLoading">Iniciando sesión...</span>
              <span v-else>Iniciar Sesión</span>
            </button>
          </form>

          <div class="login-links">
            <p>¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link></p>
            <router-link to="/" class="btn btn-secondary btn-block">
              Volver al Inicio
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

export default {
  name: 'LoginView',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const form = ref({
      email: '',
      password: ''
    })

    const handleLogin = async () => {
      try {
        await authStore.login(form.value)
        
        // Redirigir según el rol
        if (authStore.isAdmin) {
          router.push('/admin')
        } else {
          router.push('/products')
        }
      } catch (error) {
        // El error ya está manejado en el store
      }
    }

    return {
      form,
      authStore,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login {
  padding: 40px 0;
  background: var(--light-gray);
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: var(--white);
  padding: 40px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  text-align: center;
  color: var(--primary-green);
  margin-bottom: 10px;
}

.login-subtitle {
  text-align: center;
  color: var(--dark-gray);
  margin-bottom: 30px;
}

.login-form {
  margin-bottom: 30px;
}

.btn-block {
  width: 100%;
  margin-bottom: 15px;
}

.login-links {
  text-align: center;
}

.login-links a {
  color: var(--primary-green);
  text-decoration: none;
}

.login-links a:hover {
  text-decoration: underline;
}
</style>