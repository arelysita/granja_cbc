<template>
  <div class="profile">
    <div class="container">
      <h1>Mi Perfil</h1>
      
      <div class="profile-content">
        <div class="profile-card">
          <h2>Información Personal</h2>
          
          <form @submit.prevent="updateProfile" class="profile-form">
            <div class="form-group">
              <label class="form-label">Nombre Completo</label>
              <input
                v-model="form.nombre"
                type="text"
                class="form-control"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Email</label>
              <input
                v-model="form.email"
                type="email"
                class="form-control"
                required
              >
            </div>

            <div class="form-group">
              <label class="form-label">Teléfono</label>
              <input
                v-model="form.telefono"
                type="tel"
                class="form-control"
              >
            </div>

            <div class="form-group">
              <label class="form-label">Dirección</label>
              <textarea
                v-model="form.direccion"
                class="form-control"
                rows="3"
                placeholder="Tu dirección de entrega"
              ></textarea>
            </div>

            <div v-if="authStore.error" class="alert alert-error">
              {{ authStore.error }}
            </div>

            <div v-if="successMessage" class="alert alert-success">
              {{ successMessage }}
            </div>

            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="authStore.isLoading"
            >
              <span v-if="authStore.isLoading">Guardando...</span>
              <span v-else>Actualizar Perfil</span>
            </button>
          </form>
        </div>

        <div class="profile-sidebar">
          <div class="info-card">
            <h3>Información de la Cuenta</h3>
            <div class="info-item">
              <strong>Rol:</strong>
              <span class="badge" :class="authStore.user.rol">
                {{ authStore.user.rol }}
              </span>
            </div>
            <div class="info-item">
              <strong>Miembro desde:</strong>
              <span>{{ formatDate(authStore.user.fecha_creacion) }}</span>
            </div>
            <div class="info-item">
              <strong>Estado:</strong>
              <span class="badge active">Activo</span>
            </div>
          </div>

          <div class="actions-card">
            <h3>Acciones</h3>
            <button @click="authStore.logout()" class="btn btn-secondary btn-block">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import dayjs from 'dayjs'

export default {
  name: 'ProfileView',
  setup() {
    const authStore = useAuthStore()
    const successMessage = ref('')
    const form = ref({
      nombre: '',
      email: '',
      telefono: '',
      direccion: ''
    })

    const loadUserData = () => {
      if (authStore.user) {
        form.value = {
          nombre: authStore.user.nombre || '',
          email: authStore.user.email || '',
          telefono: authStore.user.telefono || '',
          direccion: authStore.user.direccion || ''
        }
      }
    }

    const updateProfile = async () => {
      successMessage.value = ''
      try {
        await authStore.updateProfile(form.value)
        successMessage.value = 'Perfil actualizado exitosamente'
        
        // Ocultar mensaje después de 3 segundos
        setTimeout(() => {
          successMessage.value = ''
        }, 3000)
      } catch (error) {
        // El error ya está manejado en el store
      }
    }

    const formatDate = (dateString) => {
      return dayjs(dateString).format('DD [de] MMMM [de] YYYY')
    }

    onMounted(() => {
      loadUserData()
    })

    return {
      authStore,
      form,
      successMessage,
      updateProfile,
      formatDate
    }
  }
}
</script>

<style scoped>
.profile {
  padding: 40px 0;
}

.profile-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  margin-top: 30px;
}

.profile-card {
  background: var(--white);
  padding: 30px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.profile-card h2 {
  margin-bottom: 25px;
  color: var(--primary-green);
  border-bottom: 2px solid var(--light-green);
  padding-bottom: 10px;
}

.profile-form {
  max-width: 500px;
}

.profile-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-card, .actions-card {
  background: var(--white);
  padding: 25px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.info-card h3, .actions-card h3 {
  margin-bottom: 20px;
  color: var(--text-dark);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--medium-gray);
}

.info-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.badge.administrador {
  background: var(--primary-green);
  color: var(--white);
}

.badge.cliente {
  background: var(--light-gray);
  color: var(--text-dark);
}

.badge.active {
  background: var(--success);
  color: var(--white);
}

@media (max-width: 768px) {
  .profile-content {
    grid-template-columns: 1fr;
  }
}
</style>