<template>
  <!-- Tarjeta principal del producto -->
  <div class="product-card">
    <div class="product-image">
      <!-- Enlace a la página de detalles del producto -->
      <router-link :to="{ name: 'ProductDetail', params: { id: product.id } }">
        <!-- Imagen del producto con el manejo de URL y fallback -->
        <img 
          :src="getImageUrl()" 
          @error="handleImageError" 
          :alt="product.nombre"
        />
      </router-link>
      <span v-if="product.stock === 0" class="out-of-stock">Agotado</span>
    </div>
    
    <div class="product-info">
      <h3 class="product-title">{{ product.nombre }}</h3>
      <p class="product-description">{{ getDescription() }}</p>
      <div class="product-meta">
        <span class="product-price">${{ getPrice() }}</span> 
        <span class="product-stock" :class="{ 'low-stock': isLowStock() }">
          Stock: {{ product.stock }}
        </span>
      </div>
      
      <div class="product-actions">
        <router-link 
          :to="{ name: 'ProductDetail', params: { id: product.id } }" 
          class="btn btn-secondary btn-small"
        >
          Ver Detalles
        </router-link>
        
        <!-- Botón para agregar al carrito, solo visible para clientes con stock -->
        <button 
          v-if="isClient && product.stock > 0"
          @click="addToCart"
          class="btn btn-primary btn-small"
          :disabled="addingToCart"
        >
          <span v-if="addingToCart">Agregando...</span>
          <span v-else>🛒 Agregar</span>
        </button>
      </div>
    </div>

    <!-- Notificación Toast para mensajes de éxito o error -->
    <transition name="toast">
      <div v-if="toast.show" :class="['toast', toast.type]">
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
// Asegúrate de que las rutas a tus stores sean correctas
import { useAuthStore } from '../../store/auth'
import { useCartStore } from '../../store/cart'

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true,
      default: () => ({})
    }
  },
  setup(props) {
    const authStore = useAuthStore()
    const cartStore = useCartStore()
    const addingToCart = ref(false)

    // Placeholder SVG en Base64
    const placeholderBase64 = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjhmOWZhIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZpbGw9IiM2Yzc1N2QiPkltYWdlbiBObyBEaXNwb25pYmxlPC90eHR+PC9zdmc+'
    const toast = ref({ show: false, message: '', type: '' })
    
    /** Lógica de la Notificación Toast **/
    const showToast = (message, type = 'success', duration = 2000) => {
      toast.value = { show: true, message, type }
      setTimeout(() => { toast.value.show = false }, duration)
    }
    
    /** Lógica de Imágenes (Manteniendo tu versión) **/
    const getImageUrl = () => {
      if (!props.product || !props.product.imagen_url) return placeholderBase64
      const imgUrl = props.product.imagen_url
      
      // Si la URL es la ruta completa del servidor Flask, la usa
      if (imgUrl.startsWith('/static/uploads/')) return `http://localhost:5000${imgUrl}`
      
      // Si solo es el nombre del archivo, construye la ruta completa
      if (!imgUrl.startsWith('http') && !imgUrl.startsWith('/')) return `http://localhost:5000/static/uploads/${imgUrl}`

      // Devuelve la URL tal cual si es una URL absoluta (http/https)
      return imgUrl
    }
    
    const handleImageError = (event) => {
      event.target.src = placeholderBase64
    }
    
    /** Lógica de Metadatos y Display **/
    const getDescription = () => props.product?.descripcion || 'Sin descripción disponible'
    
    const getPrice = () => {
        const price = props.product?.precio ?? 0;
        return parseFloat(price).toFixed(2); 
    }
    
    const isLowStock = () => props.product?.stock < 10

    /** Lógica del Carrito **/
    const addToCart = async () => {
      const productId = props.product?.id; 
      const quantity = 1;

      // Validación para evitar llamadas a la API con IDs nulos/inválidos
      if (!productId || isNaN(parseInt(productId)) || parseInt(productId) <= 0) {
        showToast('Error de datos: ID de producto no numérico o faltante.', 'error');
        return;
      }

      // Requerir autenticación
      if (!authStore.isAuthenticated) {
        window.location.href = '/login';
        return;
      }

      addingToCart.value = true;
      try {
        // Llama a la acción del store (que a su vez llama a cartService)
        await cartStore.addItem(props.product, quantity); 
        showToast('Producto agregado al carrito ✅', 'success');
        // El addItem ya llama a fetchCart dentro del store, pero lo mantenemos por si acaso
      } catch (error) {
        console.error('Error adding to cart:', error);
        // Captura el mensaje de error del backend (e.g., stock insuficiente)
        const msg = error.response?.data?.error || error.response?.data?.message || error.message || 'Error al agregar al carrito';
        showToast(msg, 'error');
      } finally {
        addingToCart.value = false;
      }
    }

    return {
      isClient: computed(() => authStore.isClient),
      addingToCart,
      getImageUrl,
      handleImageError,
      getDescription,
      getPrice,
      isLowStock,
      addToCart,
      toast
    }
  }
}
</script>

<style scoped>
/* Estilos para una apariencia moderna y responsiva */
.product-card { 
  background: #fff; 
  border-radius: 12px; 
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); 
  overflow: hidden; 
  transition: transform 0.3s, box-shadow 0.3s; 
  display: flex;
  flex-direction: column;
}
.product-card:hover { 
  transform: translateY(-5px); 
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); 
}
.product-image { 
  position: relative; 
  height: 200px; 
  overflow: hidden; 
}
.product-image img { 
  width: 100%; 
  height: 100%; 
  object-fit: cover; 
  transition: transform 0.5s; 
}
.product-card:hover .product-image img { 
  transform: scale(1.05); 
}
.out-of-stock { 
  position: absolute; 
  top: 10px; 
  right: 10px; 
  background: #c0392b; /* Rojo más fuerte */
  color: white; 
  padding: 5px 10px; 
  border-radius: 20px; 
  font-size: 12px; 
  font-weight: bold; 
}
.product-info { 
  padding: 20px; 
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* Permite que la info crezca y empuje las acciones hacia abajo */
}
.product-title { 
  font-size: 1.2rem; 
  font-weight: bold; 
  margin-bottom: 5px; 
  color: #2c3e50; 
}
.product-description { 
  color: #7f8c8d; 
  margin-bottom: 15px; 
  font-size: 0.9rem; 
  line-height: 1.4; 
  height: 3.6em; /* 3 líneas */
  overflow: hidden; 
}
.product-meta { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-top: auto; /* Empuja los metadatos y acciones al fondo */
  margin-bottom: 15px; 
  border-top: 1px solid #ecf0f1;
  padding-top: 15px;
}
.product-price { 
  font-size: 1.3rem; 
  font-weight: bold; 
  color: #27ae60; 
}
.product-stock { 
  font-size: 0.8rem; 
  color: #7f8c8d; 
}
.low-stock { 
  color: #f39c12; 
  font-weight: bold; 
}
.product-actions { 
  display: flex; 
  gap: 10px; 
  width: 100%;
}
.btn-small { 
  padding: 10px 15px; 
  font-size: 0.9rem; 
  flex: 1; 
  border-radius: 8px; 
  cursor: pointer; 
  transition: background-color 0.3s, opacity 0.3s; 
  text-decoration: none;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}
.btn-primary { 
  background-color: #2ecc71; 
  color: white; 
  border: none; 
}
.btn-primary:hover:not([disabled]) { 
  background-color: #27ae60; 
}
.btn-primary[disabled] { 
  background-color: #bdc3c7; 
  cursor: not-allowed; 
  opacity: 0.7;
}
.btn-secondary { 
  background-color: #ecf0f1; 
  color: #34495e; 
  border: 1px solid #bdc3c7; 
}
.btn-secondary:hover { 
  background-color: #e0e6e8; 
}

/* Estilos de la notificación Toast */
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #2ecc71;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  z-index: 1000;
  min-width: 250px;
  text-align: center;
  font-weight: bold;
}
.toast.error { background: #e74c3c; }
.toast-enter-active, .toast-leave-active { transition: opacity 0.3s ease; }
.toast-leave-active { position: absolute; }
.toast-enter-from, .toast-leave-to { opacity: 0; }
</style>
