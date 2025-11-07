<template>
  <div class="products-management">
    <div class="page-header">
      <h2>Gestión de Productos</h2>
      <!-- ELIMINADO: Botón Agregar Producto -->
    </div>

    <!-- ELIMINADO: FORMULARIO AGREGAR -->

    <!-- filtros -->
    <div class="filters">
      <input v-model="filters.search" type="text" placeholder="Buscar productos..." class="form-control" @input="loadProducts" />
      <select v-model="filters.category" @change="loadProducts" class="form-control">
        <option value="">Todas las categorías</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.nombre }}</option>
      </select>
      <select v-model="filters.status" @change="loadProducts" class="form-control">
        <option value="">Todos los estados</option>
        <option value="active">Activos</option>
        <option value="inactive">Inactivos</option>
      </select>
    </div>

    <!-- tabla -->
    <div class="table-container">
      <table class="products-table">
        <thead>
          <tr>
            <th>Imagen</th>
            <th>Nombre</th>
            <th>Categoría</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          <template v-for="product in products" :key="product.id">
            <tr>
              <td class="image-cell">
                <img
                  :src="getImageUrl(product.imagen_url)"
                  alt="imagen producto"
                  class="product-thumb"
                  @error="handleImageError"
                />
              </td>
              <td>
                <strong>{{ product.nombre }}</strong>
                <p class="product-description">{{ truncateDescription(product.descripcion) }}</p>
              </td>
              <td>{{ product.categoria_nombre }}</td>
              <td>${{ product.precio ? product.precio.toLocaleString('es-CL', { minimumFractionDigits: 2 }) : '0.00' }}</td>
              <td :class="{ 'low-stock': product.stock < 10 }">{{ product.stock }}</td>
              <td>
                <span class="status-badge" :class="product.activo ? 'active' : 'inactive'">
                  {{ product.activo ? 'Activo' : 'Inactivo' }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button @click="openEdit(product)" class="btn btn-small btn-secondary">✏️</button>
                  <button @click="confirmToggleStatus(product)" class="btn btn-small" :class="product.activo ? 'btn-warning' : 'btn-success'">
                    {{ product.activo ? '❌' : '✅' }}
                  </button>
                  <button @click="openStock(product)" class="btn btn-small btn-primary">📦</button>
                </div>
              </td>
            </tr>

            <!-- fila edit (debajo del producto) -->
            <tr v-if="editingId === product.id">
              <td colspan="7" class="edit-section">
                <div class="edit-card">
                  <h3>Editar Producto: {{ product.nombre }}</h3>
                  <form @submit.prevent="submitEdit">
                    <div class="form-row">
                      <div class="form-group">
                        <label>Nombre *</label>
                        <input v-model="productForm.nombre" type="text" required class="form-control" />
                      </div>
                      <div class="form-group">
                        <label>Precio *</label>
                        <input v-model.number="productForm.precio" type="number" step="0.01" required class="form-control" />
                      </div>
                      <div class="form-group">
                        <label>Stock *</label>
                        <input v-model.number="productForm.stock" type="number" required class="form-control" />
                      </div>
                      <div class="form-group">
                        <label>Categoría *</label>
                        <select v-model="productForm.categoria_id" required class="form-control">
                          <option value="">Seleccionar categoría</option>
                          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.nombre }}</option>
                        </select>
                      </div>
                    </div>

                    <div class="form-group">
                      <label>Descripción</label>
                      <textarea v-model="productForm.descripcion" class="form-control" rows="3"></textarea>
                    </div>

                    <div class="form-group">
                      <label>Imagen (opcional)</label>
                      <!-- Referencia para limpieza -->
                      <input type="file" ref="imageInputEdit" accept="image/*" @change="handleImageFile" class="form-control" /> 
                      
                      <div v-if="previewSrc" class="preview-container">
                        <img :src="previewSrc" class="image-preview" @error="handleImageError" />
                        <!-- Botón para eliminar la imagen actual (o la seleccionada) -->
                        <button type="button" v-if="productForm.imagen_url || productForm.imagen" @click="removeImage" class="btn btn-small btn-danger mt-2">
                            Eliminar Imagen Actual
                        </button>
                      </div>
                      <small class="form-text">Dejar el campo vacío y presionar "Guardar" mantiene la imagen actual. Usa el botón "Eliminar" para quitarla.</small>
                    </div>

                    <div class="form-group">
                      <label><input type="checkbox" v-model="productForm.activo" /> Producto activo</label>
                    </div>

                    <div class="modal-actions">
                      <button type="button" @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
                      <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Guardando...' : 'Guardar' }}</button>
                    </div>
                  </form>
                </div>
              </td>
            </tr>

            <!-- fila stock (debajo del producto) -->
            <tr v-if="stockOpenId === product.id">
              <td colspan="7" class="stock-section">
                <div class="stock-card">
                  <h3>Gestión de Stock - {{ product.nombre }}</h3>
                  <form @submit.prevent="submitStock">
                    <div class="form-group">
                      <label>Tipo de movimiento</label>
                      <select v-model="stockForm.tipo" required class="form-control">
                        <option value="entrada">Entrada (Aumentar)</option>
                        <option value="salida">Salida (Disminuir)</option>
                        <option value="ajuste">Ajuste (Fijar nuevo total)</option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label>Cantidad *</label>
                      <input v-model.number="stockForm.cantidad" type="number" required class="form-control" />
                      <small class="form-text">Para Entrada/Salida: Cantidad a sumar/restar. Para Ajuste: Nuevo valor de stock total.</small>
                    </div>
                    <div class="form-group">
                      <label>Motivo</label>
                      <input v-model="stockForm.motivo" type="text" class="form-control" />
                    </div>
                    <div class="modal-actions">
                      <button type="button" @click="closeStock" class="btn btn-secondary">Cancelar</button>
                      <button type="submit" class="btn btn-primary" :disabled="updatingStock">{{ updatingStock ? 'Actualizando...' : 'Actualizar Stock' }}</button>
                    </div>
                  </form>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { productService } from '../../services/productService'
import { adminService } from '../../services/adminService'

export default {
  name: 'ProductsManagement',
  setup () {
    // Configuración de URL base
    const backendUrl = 'http://localhost:5000'

    // Estados reactivos principales
    const products = ref([])
    const categories = ref([])
    const filters = reactive({ search: '', category: '', status: '' })

    // Estados de UI
    // showAddForm ELIMINADO
    const editingId = ref(null)        
    const stockOpenId = ref(null)      
    
    // Referencias a los inputs de archivo
    // imageInputCreate ELIMINADO
    const imageInputEdit = ref(null);

    // Banderas de estado
    const saving = ref(false)
    const updatingStock = ref(false)
    const deleteCurrentImage = ref(false) // Bandera para eliminar imagen en edición

    // Estado del formulario (usado solo para Editar/Stock)
    const productForm = reactive({
      id: null,
      nombre: '',
      descripcion: '',
      precio: 0,
      stock: 0,
      categoria_id: '',
      activo: true,
      imagen: null,       // Objeto File para subir
      imagen_url: ''      // URL o nombre de la imagen existente
    })

    // Estado del formulario de stock
    const stockForm = reactive({ tipo: 'entrada', cantidad: 0, motivo: '' })

    // Estado de la vista previa de la imagen
    const previewSrc = ref(null)

    // ----------------------------------------------------------------------
    // IMAGEN HELPERS
    // ----------------------------------------------------------------------
    const getImageUrl = (imagen_url) => {
      if (!imagen_url) return `${backendUrl}/static/uploads/default.jpg`
      if (imagen_url.startsWith('http')) return imagen_url
      if (imagen_url.startsWith('/static/uploads/')) return `${backendUrl}${imagen_url}`
      return `${backendUrl}/static/uploads/${imagen_url}`
    }
    const handleImageError = (e) => { e.target.src = `${backendUrl}/static/uploads/default.jpg` }

    const handleImageFile = (e) => {
      deleteCurrentImage.value = false; // Si se carga un nuevo archivo, no se elimina el existente
      const f = e.target.files && e.target.files[0]
      if (!f) {
        // Caso: no se seleccionó archivo (ej. al cancelar la selección)
        productForm.imagen = null;
        // Restaurar preview a la imagen_url existente si la hay
        previewSrc.value = productForm.imagen_url ? getImageUrl(productForm.imagen_url) : null;
        return;
      }
      
      productForm.imagen = f
      // Crea un URL temporal para la vista previa
      if (previewSrc.value) { URL.revokeObjectURL(previewSrc.value) }
      previewSrc.value = URL.createObjectURL(f)
    }
    
    const removeImage = () => {
        productForm.imagen = null;
        productForm.imagen_url = '';
        deleteCurrentImage.value = true;
        
        // Limpiar preview y URL temporal
        if (previewSrc.value) { URL.revokeObjectURL(previewSrc.value); previewSrc.value = null }
        
        // Limpiar input de archivo en el DOM (solo para edición, el de crear fue eliminado)
        nextTick(() => {
            if (editingId.value && imageInputEdit.value) {
                imageInputEdit.value.value = '';
            }
        });
    }

    // ----------------------------------------------------------------------
    // CARGAS DE DATOS
    // ----------------------------------------------------------------------
    const loadProducts = async () => {
      try {
        const params = { page: 1, per_page: 100, ...filters } 
        const data = await productService.getProducts(params)
        // Se asume que el backend mapea la categoría_nombre
        products.value = data.products || data
        
        // Agregando mapeo si el backend no lo hace (para mantener funcionalidad con el array categories)
        products.value = (data.products || data).map(p => ({
            ...p,
            categoria_nombre: categories.value.find(c => c.id === p.categoria_id)?.nombre || 'N/A'
        }));
        
      } catch (err) {
        console.error('Error al cargar productos:', err)
      }
    }
    const loadCategories = async () => {
      try {
        const data = await productService.getCategories()
        categories.value = data.categories || data
      } catch (err) {
        console.error('Error al cargar categorías:', err)
      }
    }

    // ----------------------------------------------------------------------
    // GESTIÓN DE FORMULARIOS Y UI
    // ----------------------------------------------------------------------
    
    const resetForm = () => {
      productForm.id = null
      productForm.nombre = ''
      productForm.descripcion = ''
      productForm.precio = 0
      productForm.stock = 0
      productForm.categoria_id = ''
      productForm.activo = true
      productForm.imagen = null
      productForm.imagen_url = ''
      deleteCurrentImage.value = false;
      
      // Limpiar input de archivo en el DOM de edición
      if (imageInputEdit.value) { imageInputEdit.value.value = ''; }
      
      if (previewSrc.value) { URL.revokeObjectURL(previewSrc.value); previewSrc.value = null }
    }
    
    // toggleAddForm ELIMINADO

    const openEdit = (product) => {
      if (editingId.value === product.id) {
        cancelEdit()
        return
      }
      editingId.value = product.id
      
      // Mapear datos al formulario
      productForm.id = product.id
      productForm.nombre = product.nombre
      productForm.descripcion = product.descripcion
      productForm.precio = Number(product.precio)
      productForm.stock = Number(product.stock)
      productForm.categoria_id = product.categoria_id
      productForm.activo = !!product.activo
      productForm.imagen = null
      productForm.imagen_url = product.imagen_url || ''
      deleteCurrentImage.value = false;
      
      // Mostrar imagen existente
      previewSrc.value = product.imagen_url ? getImageUrl(product.imagen_url) : null
      
      stockOpenId.value = null // Cierra stock
      
      // Limpiar el input de archivo al abrir la edición
      if(imageInputEdit.value) {
          nextTick(() => { imageInputEdit.value.value = ''; });
      }
    }

    const cancelEdit = () => {
      editingId.value = null
      resetForm()
    }
    
    // GESTIÓN DE STOCK
    const openStock = (product) => {
      if (stockOpenId.value === product.id) {
        stockOpenId.value = null
        return
      }
      stockOpenId.value = product.id
      editingId.value = null // Cierra edición
      stockForm.tipo = 'entrada'
      stockForm.cantidad = 0
      stockForm.motivo = ''
    }

    const closeStock = () => { stockOpenId.value = null }
    
    const submitStock = async () => {
      if (!stockOpenId.value) return
      updatingStock.value = true
      try {
        await adminService.addStockMovement({
          producto_id: stockOpenId.value,
          tipo: stockForm.tipo,
          cantidad: stockForm.cantidad,
          motivo: stockForm.motivo
        })
        await loadProducts()
        closeStock()
      } catch (err) {
        console.error('Error al actualizar stock:', err)
      } finally {
        updatingStock.value = false
      }
    }


    // ----------------------------------------------------------------------
    // SUBMIT ACTIONS
    // ----------------------------------------------------------------------
    
    // submitCreate ELIMINADO
    
    const submitEdit = async () => {
      if (!editingId.value || !productForm.nombre || !productForm.categoria_id) {
        console.error("Los campos ID, Nombre y Categoría son obligatorios para editar.");
        return;
      }
      
      saving.value = true;
      try {
        const fd = new FormData();
        
        // CORRECCIÓN: Usamos toString() para asegurar que los campos vayan como cadenas válidas
        fd.append('nombre', productForm.nombre.toString());
        fd.append('categoria_id', productForm.categoria_id.toString());
        fd.append('precio', productForm.precio.toString());
        fd.append('stock', productForm.stock.toString());

        fd.append('descripcion', productForm.descripcion || '');
        fd.append('activo', productForm.activo ? 'true' : 'false'); 
        
        if (productForm.imagen) {
            fd.append('imagen', productForm.imagen);
        } else if (deleteCurrentImage.value) {
            fd.append('delete_image', 'true');
        } 

        await productService.updateProduct(editingId.value, fd); 
        await loadProducts();
        cancelEdit();
      } catch (err) {
        console.error('Error al actualizar el producto:', err.response?.data?.error || err);
      } finally {
        saving.value = false;
        // Limpiar URL temporal de preview
        if (previewSrc.value && productForm.imagen) { URL.revokeObjectURL(previewSrc.value); previewSrc.value = null; }
      }
    };

    // CAMBIO DE ESTADO
    const confirmToggleStatus = async (product) => {
      // Uso de window.confirm para cumplir con las restricciones.
      const action = product.activo ? 'desactivar' : 'activar';
      // NOTA: Usar un modal en la UI es la práctica recomendada
      const ok = window.confirm(`¿Deseas ${action} el producto "${product.nombre}"?`) 
      if (!ok) return
      try {
        // El servicio maneja la inyección del token.
        await productService.updateProduct(product.id, { activo: !product.activo })
        await loadProducts()
      } catch (err) {
        console.error(`Error al ${action} el producto`, err)
      }
    }

    // UTILIDADES
    const truncateDescription = (t) => (t ? (t.length > 50 ? t.slice(0, 50) + '...' : t) : '')

    // ----------------------------------------------------------------------
    // LIFECYCLE HOOK
    // ----------------------------------------------------------------------
    onMounted(() => {
      loadProducts()
      loadCategories()
    })

    return {
      // Data y Estado
      products, categories, filters,
      imageInputEdit,
      editingId, stockOpenId,
      productForm, stockForm, saving, updatingStock, previewSrc,
      
      // Métodos
      getImageUrl, handleImageError, handleImageFile, removeImage,
      loadProducts, loadCategories, 
      openEdit, cancelEdit, submitEdit,
      confirmToggleStatus, 
      openStock, submitStock, closeStock,
      truncateDescription
    }
  }
}
</script>

<style scoped>
/* ESTILOS DE GESTIÓN DE PRODUCTOS */

.products-management {
  padding: 20px;
  background-color: #f7f9fc;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 15px;
}

h2 {
  font-size: 1.8rem;
  color: #333;
  margin: 0;
}

/* Botones genéricos */
.btn {
  padding: 10px 15px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s, transform 0.1s;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { background-color: #007bff; color: white; }
.btn-secondary { background-color: #6c757d; color: white; }
.btn-success { background-color: #28a745; color: white; }
.btn-warning { background-color: #ffc107; color: #333; }
.btn-danger { background-color: #dc3545; color: white; }
.btn-small { padding: 6px 10px; font-size: 0.85rem; margin: 0 4px; }

/* Filtros */
.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 25px;
  padding: 15px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.form-control {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
}

/* Tabla */
.table-container { 
    overflow-x: auto; 
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
.products-table { 
    width: 100%; 
    border-collapse: collapse; 
}
.products-table thead {
    background-color: #f1f1f1;
}
.products-table th, .products-table td { 
    padding: 15px 10px; 
    border-bottom: 1px solid #eee; 
    vertical-align: middle; 
    text-align: left;
    font-size: 0.95rem;
}
.products-table th:last-child, .products-table td:last-child {
    text-align: center;
    width: 150px;
}

.image-cell { width: 100px; text-align: center; }
.product-thumb { 
    width: 70px; 
    height: 70px; 
    object-fit: cover; 
    border-radius: 6px; 
    border: 1px solid #ddd;
    background: #f5f5f5; 
}
.product-description { 
    margin: 4px 0 0; 
    color: #888; 
    font-size: 0.85rem; 
}

.low-stock {
    font-weight: 700;
    color: #dc3545; /* Rojo */
}

/* Badges de estado */
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
}
.status-badge.active { background-color: #e6ffed; color: #2e7d32; }
.status-badge.inactive { background-color: #ffe0e0; color: #d32f2f; }

.action-buttons { 
    display: flex;
    justify-content: center;
}

/* Secciones de Formulario */
.edit-section td, .stock-section td { 
    padding: 0;
    border: none;
}
.edit-card, .stock-card { 
    padding: 20px; 
    border: 1px solid #c7c7c7; 
    border-radius: 8px; 
    background: #ffffff; 
    margin: 15px; 
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

/* Estructura del Formulario */
.form-row {
    display: flex;
    gap: 20px;
    margin-bottom: 15px;
}
.form-group {
    flex: 1;
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
}
label {
    font-weight: 600;
    margin-bottom: 5px;
    color: #555;
}
textarea.form-control {
    resize: vertical;
}

.modal-actions { 
    margin-top: 20px; 
    display:flex; 
    gap:10px; 
    justify-content: flex-end;
}

/* Previsualización de Imagen */
.preview-container {
    margin-top: 10px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.image-preview { 
    width: 100px; 
    height: 100px; 
    object-fit: cover; 
    border-radius: 8px; 
    border: 1px solid #ddd;
    margin-bottom: 5px;
}

.mt-2 { margin-top: 8px; }
.form-text { font-size: 0.8rem; color: #888; }

/* Responsive */
@media (max-width: 900px) {
  .form-row {
    flex-direction: column;
  }
  .filters {
    flex-direction: column;
  }
  .filters .form-control {
    max-width: 100%;
  }
  .products-table th, .products-table td {
      padding: 10px 5px;
  }
}
</style>
