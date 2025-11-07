// Archivo creado automáticamente
<template>
  <div class="products">
    <div class="container">
      <!-- Filtros y Búsqueda -->
      <div class="products-header">
        <h1>Nuestros Productos</h1>
        
        <div class="products-controls">
          <div class="search-box">
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Buscar productos..."
              class="form-control"
              @input="handleSearch"
            >
          </div>
          
          <select v-model="selectedCategory" @change="loadProducts" class="form-control">
            <option value="">Todas las categorías</option>
            <option 
              v-for="category in categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.nombre }}
            </option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        <p>Cargando productos...</p>
      </div>

      <!-- Productos -->
      <div v-else class="products-grid">
        <div v-if="products.length === 0" class="no-products">
          <p>No se encontraron productos.</p>
        </div>
        
        <ProductCard 
          v-else
          v-for="product in products" 
          :key="product.id"
          :product="product"
        />
      </div>

      <!-- Paginación -->
      <div v-if="pagination.pages > 1" class="pagination">
        <button 
          @click="changePage(pagination.current_page - 1)"
          :disabled="pagination.current_page === 1"
          class="btn btn-secondary"
        >
          Anterior
        </button>
        
        <span class="pagination-info">
          Página {{ pagination.current_page }} de {{ pagination.pages }}
        </span>
        
        <button 
          @click="changePage(pagination.current_page + 1)"
          :disabled="pagination.current_page === pagination.pages"
          class="btn btn-secondary"
        >
          Siguiente
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { productService } from '../services/productService'
import ProductCard from '../components/products/ProductCard.vue'

export default {
  name: 'ProductsView',
  components: {
    ProductCard
  },
  setup() {
    const products = ref([])
    const categories = ref([])
    const loading = ref(true)
    const searchTerm = ref('')
    const selectedCategory = ref('')
    
    const pagination = ref({
      current_page: 1,
      pages: 1,
      total: 0
    })

    let searchTimeout = null

    const loadProducts = async (page = 1) => {
      loading.value = true
      try {
        const params = {
          page,
          per_page: 12
        }

        if (selectedCategory.value) {
          params.categoria_id = selectedCategory.value
        }

        if (searchTerm.value) {
          params.search = searchTerm.value
        }

        const data = await productService.getProducts(params)
        products.value = data.products
        pagination.value = {
          current_page: data.current_page,
          pages: data.pages,
          total: data.total
        }
         // ✅ AÑADE ESTOS CONSOLE.LOG AQUÍ
        console.log('📦 PRODUCTOS CARGADOS DESDE EL BACKEND:')
        data.products.forEach((product, index) => {
          console.log(`Producto ${index + 1}:`, {
            nombre: product.nombre,
            imagen_url: product.imagen_url,
            id: product.id
        })
        })
      } catch (error) {
        console.error('Error loading products:', error)
      } finally {
        loading.value = false
      }
    }

    const loadCategories = async () => {
      try {
        const data = await productService.getCategories()
        categories.value = data.categories
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    }

    const handleSearch = () => {
      // Debounce search
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        loadProducts(1)
      }, 500)
    }

    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.pages) {
        loadProducts(page)
      }
    }

    onMounted(() => {
      loadProducts()
      loadCategories()
    })

    return {
      products,
      categories,
      loading,
      searchTerm,
      selectedCategory,
      pagination,
      loadProducts,
      handleSearch,
      changePage
    }
  }
}
</script>

<style scoped>
.products {
  padding: 40px 0;
}

.products-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.products-header h1 {
  color: var(--primary-green);
  margin: 0;
}

.products-controls {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.search-box {
  min-width: 250px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.no-products {
  text-align: center;
  padding: 60px 20px;
  color: var(--dark-gray);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.pagination-info {
  color: var(--dark-gray);
  font-weight: 500;
}

@media (max-width: 768px) {
  .products-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .products-controls {
    flex-direction: column;
  }
  
  .search-box {
    min-width: auto;
  }
}
</style>