<template>
  <div class="register">
    <div class="container">
      <div class="register-container">
        <div class="register-card">
          <h2>Crear Cuenta</h2>
          <p class="register-subtitle">Únete a Granja CBC y descubre productos frescos</p>

          <form @submit.prevent="handleRegister" class="register-form">
            <div class="form-group">
              <label class="form-label">Nombre Completo</label>
              <input
                v-model="form.nombre"
                type="text"
                class="form-control"
                placeholder="Tu nombre completo"
                required
              >
            </div>

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
              <label class="form-label">Teléfono</label>
              <input
                v-model="form.telefono"
                type="tel"
                class="form-control"
                placeholder="Tu número de teléfono"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Dirección</label>
              <textarea
                v-model="form.direccion"
                class="form-control"
                placeholder="Tu dirección de entrega"
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Contraseña</label>
              <input
                v-model="form.password"
                type="password"
                class="form-control"
                placeholder="Crea una contraseña segura"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Confirmar Contraseña</label>
              <input
                v-model="form.password_confirmation"
                type="password"
                class="form-control"
                placeholder="Repite tu contraseña"
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
              <span v-if="authStore.isLoading">Creando cuenta...</span>
              <span v-else>Crear Cuenta</span>
            </button>
          </form>

          <div class="register-links">
            <p>¿Ya tienes cuenta? <router-link to="/login">Inicia sesión aquí</router-link></p>
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
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

export default {
  name: 'RegisterView',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const form = ref({
      nombre: '',
      email: '',
      telefono: '',
      direccion: '',
      password: '',
      password_confirmation: ''
    })

    const handleRegister = async () => {
      if (form.value.password !== form.value.password_confirmation) {
        authStore.error = 'Las contraseñas no coinciden'
        return
      }

      try {
        await authStore.register(form.value)
        router.push('/products')
      } catch (error) {
        // El error ya está manejado en el store
      }
    }

    // Limpiar error cuando el usuario empiece a escribir
    watch(form, () => {
      if (authStore.error) {
        authStore.error = null
      }
    }, { deep: true })

    return {
      form,
      authStore,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register {
  padding: 40px 0;
  background: var(--light-gray);
  min-height: 100vh;
  display: flex;
  align-items: center;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-card {
  background: var(--white);
  padding: 40px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  width: 100%;
  max-width: 500px;
}

.register-card h2 {
  text-align: center;
  color: var(--primary-green);
  margin-bottom: 10px;
}

.register-subtitle {
  text-align: center;
  color: var(--dark-gray);
  margin-bottom: 30px;
}

.register-form {
  margin-bottom: 30px;
}

.btn-block {
  width: 100%;
  margin-bottom: 15px;
}

.register-links {
  text-align: center;
}

.register-links a {
  color: var(--primary-green);
  text-decoration: none;
}

.register-links a:hover {
  text-decoration: underline;
}
</style>