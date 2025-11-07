// Archivo creado automáticamente
<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Bienvenido a Granja CBC</h1>
          <p class="hero-subtitle">Productos frescos y naturales directamente de nuestra granja a tu mesa</p>
          <div class="hero-actions">
            <router-link v-if="!isAuthenticated" to="/register" class="btn btn-primary btn-large">
              Comenzar a Comprar
            </router-link>
            <router-link v-else to="/products" class="btn btn-primary btn-large">
              Ver Productos
            </router-link>
            <router-link v-if="!isAuthenticated" to="/login" class="btn btn-secondary btn-large">
              Iniciar Sesión
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <h2 class="section-title">¿Por qué elegirnos?</h2>
        <div class="grid grid-3">
          <div class="feature-card">
            <div class="feature-icon">🌱</div>
            <h3>100% Natural</h3>
            <p>Productos cultivados de manera sostenible sin químicos dañinos</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🚚</div>
            <h3>Envío Rápido</h3>
            <p>Entrega a domicilio en 24-48 horas manteniendo la frescura</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💰</div>
            <h3>Precios Justos</h3>
            <p>Directo del productor al consumidor, sin intermediarios</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section v-if="featuredProducts.length" class="featured-products">
      <div class="container">
        <h2 class="section-title">Productos Destacados</h2>
        <div class="grid grid-4">
          <ProductCard 
            v-for="product in featuredProducts" 
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="text-center mt-3">
          <router-link to="/products" class="btn btn-primary">
            Ver Todos los Productos
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { productService } from '../services/productService'
import ProductCard from '../components/products/ProductCard.vue'

export default {
  name: 'HomeView',
  components: {
    ProductCard
  },
  setup() {
    const authStore = useAuthStore()
    const featuredProducts = ref([])
    const loading = ref(true)

    const loadFeaturedProducts = async () => {
      try {
        const data = await productService.getProducts({ per_page: 8 })
        featuredProducts.value = data.products.slice(0, 4) // Mostrar solo 4 productos destacados
      } catch (error) {
        console.error('Error loading featured products:', error)
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      loadFeaturedProducts()
    })

    return {
      isAuthenticated: computed(() => authStore.isAuthenticated),
      featuredProducts,
      loading
    }
  }
}
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, var(--primary-green), var(--light-green));
  color: var(--white);
  padding: 100px 0;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 20px;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 30px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-large {
  padding: 15px 30px;
  font-size: 1.1rem;
}

.features {
  padding: 80px 0;
  background: var(--white);
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 50px;
  color: var(--primary-green);
}

.feature-card {
  text-align: center;
  padding: 30px 20px;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: var(--dark-green);
}

.feature-card p {
  color: var(--dark-gray);
  line-height: 1.6;
}

.featured-products {
  padding: 80px 0;
  background: var(--light-gray);
}
</style>