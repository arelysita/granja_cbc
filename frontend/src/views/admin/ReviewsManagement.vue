<template>
  <div class="reviews-management">
    <div class="page-header">
      <h2>Moderación de Reseñas</h2>
    </div>

    <!-- Pestañas -->
    <div class="tabs">
      <button 
        @click="activeTab = 'pending'"
        class="tab-btn"
        :class="{ active: activeTab === 'pending' }"
      >
        Pendientes ({{ pendingReviews.length }})
      </button>
      <button 
        @click="activeTab = 'approved'"
        class="tab-btn"
        :class="{ active: activeTab === 'approved' }"
      >
        Aprobadas ({{ approvedReviews.length }})
      </button>
    </div>

    <!-- Lista de Reseñas -->
    <div class="reviews-list">
      <div v-if="activeTab === 'pending' && pendingReviews.length === 0" class="no-reviews">
        <p>No hay reseñas pendientes de moderación.</p>
      </div>
      
      <div v-else-if="activeTab === 'approved' && approvedReviews.length === 0" class="no-reviews">
        <p>No hay reseñas aprobadas.</p>
      </div>

      <div v-else class="reviews-container">
        <div 
          v-for="review in currentReviews" 
          :key="review.id" 
          class="review-card"
          :class="{ pending: !review.aprobada }"
        >
          <div class="review-header">
            <div class="reviewer-info">
              <strong>{{ review.usuario_nombre }}</strong>
              <span class="review-product">Producto: {{ review.producto_nombre }}</span>
            </div>
            <div class="review-meta">
              <div class="review-rating">
                <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= review.calificacion }">
                  ★
                </span>
              </div>
              <span class="review-date">{{ formatDate(review.fecha_creacion) }}</span>
            </div>
          </div>

          <div class="review-content">
            <p class="review-comment">{{ review.comentario }}</p>
          </div>

          <div class="review-actions">
            <div v-if="!review.aprobada" class="pending-actions">
              <button 
                @click="approveReview(review)"
                class="btn btn-success btn-small"
              >
                ✅ Aprobar
              </button>
              <button 
                @click="rejectReview(review)"
                class="btn btn-danger btn-small"
              >
                ❌ Rechazar
              </button>
            </div>
            
            <div v-else class="approved-actions">
              <span class="approved-badge">✅ Aprobada</span>
              <button 
                @click="rejectReview(review)"
                class="btn btn-danger btn-small"
              >
                Desaprobar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { adminService } from '../../services/adminService'
import dayjs from 'dayjs'

export default {
  name: 'ReviewsManagement',
  setup() {
    const reviews = ref([])
    const loading = ref(false)
    const activeTab = ref('pending')

    const pendingReviews = computed(() => {
      return reviews.value.filter(review => !review.aprobada)
    })

    const approvedReviews = computed(() => {
      return reviews.value.filter(review => review.aprobada)
    })

    const currentReviews = computed(() => {
      return activeTab.value === 'pending' ? pendingReviews.value : approvedReviews.value
    })

    const loadReviews = async () => {
      loading.value = true
      try {
        // Cargar reseñas pendientes
        const pendingData = await adminService.getPendingReviews()
        
        // En una implementación real, también cargaríamos las aprobadas
        // Por ahora, simulamos con los datos disponibles
        reviews.value = pendingData.reviews
      } catch (error) {
        console.error('Error loading reviews:', error)
      } finally {
        loading.value = false
      }
    }

    const approveReview = async (review) => {
      try {
        await adminService.approveReview(review.id)
        review.aprobada = true
        alert('Reseña aprobada exitosamente!')
      } catch (error) {
        alert('Error aprobando reseña')
      }
    }

    const rejectReview = async (review) => {
      const action = review.aprobada ? 'desaprobar' : 'rechazar'
      const confirmMessage = `¿Estás seguro de que quieres ${action} esta reseña?`
      
      if (confirm(confirmMessage)) {
        try {
          // En una implementación real, aquí llamaríamos a la API para rechazar
          // Por ahora, solo actualizamos localmente
          if (review.aprobada) {
            review.aprobada = false
          } else {
            // Eliminar de la lista si está pendiente
            const index = reviews.value.findIndex(r => r.id === review.id)
            if (index !== -1) {
              reviews.value.splice(index, 1)
            }
          }
          alert(`Reseña ${action}da exitosamente!`)
        } catch (error) {
          alert(`Error ${action}ndo reseña`)
        }
      }
    }

    const formatDate = (dateString) => {
      return dayjs(dateString).format('DD/MM/YYYY HH:mm')
    }

    onMounted(() => {
      loadReviews()
    })

    return {
      reviews,
      activeTab,
      pendingReviews,
      approvedReviews,
      currentReviews,
      approveReview,
      rejectReview,
      formatDate
    }
  }
}
</script>

<style scoped>
.reviews-management {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--medium-gray);
}

.tab-btn {
  padding: 12px 24px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 1rem;
  color: var(--dark-gray);
  transition: var(--transition);
}

.tab-btn:hover {
  background: var(--light-gray);
}

.tab-btn.active {
  color: var(--primary-green);
  border-bottom-color: var(--primary-green);
  font-weight: 500;
}

.reviews-list {
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.no-reviews {
  text-align: center;
  padding: 60px 20px;
  color: var(--dark-gray);
}

.reviews-container {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-card {
  padding: 20px;
  border: 1px solid var(--medium-gray);
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.review-card.pending {
  border-left: 4px solid var(--warning);
  background: #fffbf0;
}

.review-card:hover {
  box-shadow: var(--box-shadow);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.reviewer-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.reviewer-info strong {
  color: var(--text-dark);
}

.review-product {
  font-size: 0.9rem;
  color: var(--primary-green);
  font-weight: 500;
}

.review-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.review-rating {
  display: flex;
}

.star {
  color: var(--medium-gray);
  margin-right: 2px;
}

.star.filled {
  color: var(--warning);
}

.review-date {
  font-size: 0.8rem;
  color: var(--dark-gray);
}

.review-content {
  margin-bottom: 15px;
}

.review-comment {
  line-height: 1.5;
  color: var(--text-dark);
  margin: 0;
}

.review-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pending-actions {
  display: flex;
  gap: 10px;
}

.approved-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.approved-badge {
  color: var(--success);
  font-weight: 500;
}

.btn-small {
  padding: 8px 15px;
  font-size: 0.9rem;
}

.btn-success {
  background: var(--success);
  color: var(--white);
}

.btn-danger {
  background: var(--danger);
  color: var(--white);
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
  }
  
  .review-header {
    flex-direction: column;
    gap: 15px;
  }
  
  .review-meta {
    align-items: flex-start;
  }
  
  .review-actions {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .pending-actions {
    width: 100%;
  }
  
  .pending-actions .btn {
    flex: 1;
  }
}
</style>