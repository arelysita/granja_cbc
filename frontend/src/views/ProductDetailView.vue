<template>
  <div class="product-detail">
    <div class="container">
      <div v-if="loading" class="loading">
        <p>Cargando producto...</p>
      </div>

      <div v-else-if="product" class="product-detail-content">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
          <router-link to="/products">Productos</router-link> / 
          <span>{{ product.nombre }}</span>
        </nav>

        <div class="product-layout">
          <!-- Imagen del producto -->
          <div class="product-image-section">
            <!-- CRÍTICO: Usamos productImageUrl para la ruta completa -->
            <img 
              :src="productImageUrl" 
              :alt="product.nombre"
              class="product-image"
              @error="handleImageError"
            >
          </div>

          <!-- Información del producto -->
          <div class="product-info-section">
            <h1 class="product-title">{{ product.nombre }}</h1>
            <p class="product-category">Categoría: {{ product.categoria_nombre }}</p>
            
            <div class="product-price">${{ product.precio.toLocaleString() }}</div>
            
            <div class="product-stock" :class="{ 
              'in-stock': product.stock > 0, 
              'out-of-stock': product.stock === 0 
            }">
              {{ product.stock > 0 ? `Stock disponible: ${product.stock}` : 'Agotado' }}
            </div>

            <p class="product-description">{{ product.descripcion || 'Sin descripción disponible.' }}</p>

            <!-- Acciones -->
            <div class="product-actions">
              <div v-if="product.stock > 0" class="quantity-selector">
                <label>Cantidad:</label>
                <div class="quantity-controls">
                  <button @click="decreaseQuantity" :disabled="quantity <= 1">-</button>
                  <span>{{ quantity }}</span>
                  <button @click="increaseQuantity" :disabled="quantity >= product.stock">+</button>
                </div>
              </div>

              <button 
                v-if="isClient && product.stock > 0"
                @click="addToCart"
                class="btn btn-primary btn-large"
                :disabled="addingToCart"
              >
                <span v-if="addingToCart">Agregando...</span>
                <span v-else>🛒 Agregar al Carrito</span>
              </button>

              <button 
                v-else-if="!isAuthenticated && product.stock > 0"
                @click="goToLogin"
                class="btn btn-primary btn-large"
              >
                Iniciar Sesión para Comprar
              </button>

              <div v-else class="out-of-stock-message">
                Producto temporalmente no disponible
              </div>
            </div>

            <!-- Información adicional -->
            <div class="product-features">
              <div class="feature">
                <span class="feature-icon">🚚</span>
                <span>Envío gratis en compras mayores a $50.000</span>
              </div>
              <div class="feature">
                <span class="feature-icon">↩️</span>
                <span>Devolución fácil en 30 días</span>
              </div>
              <div class="feature">
                <span class="feature-icon">📞</span>
                <span>Soporte 24/7</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Reseñas -->
        <div class="product-reviews">
          <h3>Reseñas del Producto</h3>
          <div v-if="reviews.length === 0" class="no-reviews">
            <p>Este producto aún no tiene reseñas.</p>
          </div>
          <div v-else class="reviews-list">
            <div v-for="review in reviews" :key="review.id" class="review-card">
              <div class="review-header">
                <span class="review-author">{{ review.usuario_nombre }}</span>
                <div class="review-rating">
                  <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= review.calificacion }">
                    ★
                  </span>
                </div>
              </div>
              <p class="review-comment">{{ review.comentario }}</p>
              <span class="review-date">{{ formatDate(review.fecha_creacion) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="not-found">
        <h2>Producto no encontrado</h2>
        <router-link to="/products" class="btn btn-primary">Volver a Productos</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { useCartStore } from '../store/cart'
import { productService } from '../services/productService'
import dayjs from 'dayjs'

export default {
  name: 'ProductDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const cartStore = useCartStore()

    const product = ref(null)
    const reviews = ref([])
    const loading = ref(true)
    const addingToCart = ref(false)
    const quantity = ref(1)

    // URL base del servidor Flask, necesario cuando Vue se ejecuta en otro puerto (9080)
    const BACKEND_URL = 'http://localhost:5000'

    const loadProduct = async () => {
      try {
        const productId = route.params.id
        const productData = await productService.getProduct(productId)
        product.value = productData.product

        // Cargar reseñas
        const reviewsData = await productService.getProductReviews(productId)
        reviews.value = reviewsData.reviews
      } catch (error) {
        console.error('Error loading product:', error)
        product.value = null
      } finally {
        loading.value = false
      }
    }

    // PROPIEDAD COMPUTADA CRÍTICA: Construye la URL completa de la imagen
    const productImageUrl = computed(() => {
        if (!product.value || !product.value.imagen_url) {
            // Si no hay URL en el producto, usamos el placeholder local de Vue
            return '/placeholder-product.jpg' 
        }
        
        const url = product.value.imagen_url
        
        // Asumimos que el backend envía la ruta estática ('/static/uploads/manzanas.jpg')
        // Le anteponemos la URL base del backend para que el navegador sepa dónde buscarla.
        return `${BACKEND_URL}${url}`
    })

    const increaseQuantity = () => {
      if (quantity.value < product.value.stock) {
        quantity.value++
      }
    }

    const decreaseQuantity = () => {
      if (quantity.value > 1) {
        quantity.value--
      }
    }

    const addToCart = async () => {
      if (!authStore.isAuthenticated) {
        router.push('/login')
        return
      }

      addingToCart.value = true
      try {
        await cartStore.addItem(product.value.id, quantity.value)
        // Reemplazamos alert() por una notificación modal o mensaje en el futuro, pero lo dejamos por ahora
        alert('Producto agregado al carrito exitosamente!') 
        quantity.value = 1 // Reset quantity
      } catch (error) {
        // Reemplazamos alert()
        alert(error.response?.data?.error || 'Error al agregar al carrito')
      } finally {
        addingToCart.value = false
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    const handleImageError = (event) => {
      // Si la imagen cargada por BACKEND_URL falla, usamos el placeholder local
      event.target.src = '/placeholder-product.jpg'
    }

    const formatDate = (dateString) => {
      return dayjs(dateString).format('DD/MM/YYYY')
    }

    onMounted(() => {
      loadProduct()
    })

    return {
      product,
      reviews,
      loading,
      addingToCart,
      quantity,
      isAuthenticated: computed(() => authStore.isAuthenticated),
      isClient: computed(() => authStore.isClient),
      productImageUrl, // Exportamos la propiedad computada corregida
      increaseQuantity,
      decreaseQuantity,
      addToCart,
      goToLogin,
      handleImageError,
      formatDate
    }
  }
}
</script>

<style scoped>
.product-detail {
  padding: 40px 0;
}

.breadcrumb {
  margin-bottom: 30px;
  color: var(--dark-gray);
}

.breadcrumb a {
  color: var(--primary-green);
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  margin-bottom: 50px;
}

/* Estilos de la imagen y su contenedor */
.product-image-section {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px; /* Asegura un tamaño mínimo */
    background-color: var(--light-gray);
    border-radius: var(--border-radius);
}

.product-image {
  width: 100%;
  max-width: 500px;
  /* La siguiente línea es crucial para que el placeholder se ajuste al contenedor sin estirarse */
  max-height: 500px; 
  object-fit: contain; /* Asegura que la imagen se vea completa sin distorsión */
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.product-title {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: var(--text-dark);
}

.product-category {
  color: var(--dark-gray);
  margin-bottom: 20px;
  font-size: 1.1rem;
}

.product-price {
  font-size: 2rem;
  font-weight: bold;
  color: var(--primary-green);
  margin-bottom: 15px;
}

.product-stock {
  font-weight: bold;
  margin-bottom: 20px;
  padding: 8px 15px;
  border-radius: var(--border-radius);
  display: inline-block;
}

.in-stock {
  background-color: #d4edda;
  color: #155724;
}

.out-of-stock {
  background-color: #f8d7da;
  color: #721c24;
}

.product-description {
  line-height: 1.6;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.product-actions {
  margin-bottom: 30px;
}

.quantity-selector {
  margin-bottom: 20px;
}

.quantity-selector label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.quantity-controls button {
  width: 40px;
  height: 40px;
  border: 1px solid var(--medium-gray);
  background: var(--white);
  border-radius: var(--border-radius);
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.quantity-controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.quantity-controls span {
  font-size: 1.2rem;
  font-weight: bold;
  min-width: 30px;
  text-align: center;
}

.btn-large {
  padding: 15px 30px;
  font-size: 1.1rem;
}

.out-of-stock-message {
  color: var(--danger);
  font-weight: bold;
  font-size: 1.1rem;
}

.product-features {
  border-top: 1px solid var(--medium-gray);
  padding-top: 20px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.feature-icon {
  font-size: 1.2rem;
}

.product-reviews {
  border-top: 1px solid var(--medium-gray);
  padding-top: 40px;
}

.product-reviews h3 {
  margin-bottom: 20px;
  color: var(--text-dark);
}

.no-reviews {
  text-align: center;
  padding: 40px;
  color: var(--dark-gray);
}

.review-card {
  background: var(--white);
  padding: 20px;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  margin-bottom: 20px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.review-author {
  font-weight: bold;
  color: var(--text-dark);
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

.review-comment {
  line-height: 1.5;
  margin-bottom: 10px;
}

.review-date {
  color: var(--dark-gray);
  font-size: 0.9rem;
}

.not-found {
  text-align: center;
  padding: 60px 20px;
}

.not-found h2 {
  color: var(--danger);
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .product-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .product-title {
    font-size: 2rem;
  }
  
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
