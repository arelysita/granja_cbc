// Archivo creado automáticamente
import api from './api'

const API_BASE_URL = 'http://localhost:5000'

export const productService = {
    async getProducts(params = {}) {
        try {
            console.log('🟡 Cargando productos...', params)
            const response = await api.get('/products', { params })
            console.log('✅ Productos cargados:', response.data.products?.length || response.data.length)

            // Procesar imágenes
            if (response.data && response.data.products) {
                response.data.products = response.data.products.map(product => {
                    if (product.imagen_url && !product.imagen_url.startsWith('http')) {
                        product.imagen_url = `${API_BASE_URL}${product.imagen_url.startsWith('/') ? '' : '/'}${product.imagen_url.replace(/\\/g, '/')}`
                    }
                    return product
                })
            }

            return response.data
        } catch (error) {
            console.error('❌ Error cargando productos:', error.response?.status, error.response?.data)
            throw error
        }
    },

    async getProduct(id) {
        try {
            const response = await api.get(`/products/${id}`)
            
            if (response.data && response.data.imagen_url && !response.data.imagen_url.startsWith('http')) {
                response.data.imagen_url = `${API_BASE_URL}${response.data.imagen_url.startsWith('/') ? '' : '/'}${response.data.imagen_url.replace(/\\/g, '/')}`
            }

            return response.data
        } catch (error) {
            console.error('❌ Error cargando producto:', error.response?.status)
            throw error
        }
    },

    async createProduct(formData) {
        try {
            console.log('🟡 Creando producto...')
            console.log('📦 Datos del formulario:')
            
            // Log los datos del FormData para debugging
            for (let [key, value] of formData.entries()) {
                if (key === 'imagen') {
                    console.log(`  ${key}:`, value.name, `(${value.type})`)
                } else {
                    console.log(`  ${key}:`, value)
                }
            }

            // 🚨 MODIFICACIÓN: Eliminamos el header Content-Type para peticiones FormData
            const response = await api.post('/products', formData) 
            
            console.log('✅ Producto creado exitosamente:', response.data)
            return response.data
        } catch (error) {
            console.error('❌ Error creando producto:', error.response?.status)
            console.error('📋 Detalles del error:', error.response?.data)
            throw error
        }
    },

    async updateProduct(id, data) {
        try {
            console.log('🟡 Actualizando producto...', id)
            
            let response
            if (data instanceof FormData) {
                console.log('📦 Usando FormData para actualizar')
                for (let [key, value] of data.entries()) {
                    if (key === 'imagen') {
                        console.log(`  ${key}:`, value.name, `(${value.type})`)
                    } else {
                        console.log(`  ${key}:`, value)
                    }
                }
                
                // 🚨 MODIFICACIÓN: Eliminamos el header Content-Type para peticiones FormData
                response = await api.put(`/products/${id}`, data)
            } else {
                console.log('📦 Usando JSON para actualizar:', data)
                response = await api.put(`/products/${id}`, data)
            }
            
            console.log('✅ Producto actualizado exitosamente')
            return response.data
        } catch (error) {
            console.error('❌ Error actualizando producto:', error.response?.status)
            console.error('📋 Detalles del error:', error.response?.data)
            throw error
        }
    },

    async deleteProduct(id) {
        try {
            const response = await api.delete(`/products/${id}`)
            return response.data
        } catch (error) {
            console.error('❌ Error eliminando producto:', error.response?.status)
            throw error
        }
    },

    async getProductReviews(productId) {
        try {
            const response = await api.get(`/products/${productId}/reviews`)
            return response.data
        } catch (error) {
            console.error('❌ Error cargando reseñas:', error.response?.status)
            throw error
        }
    },

    async getCategories() {
        try {
            console.log('🟡 Cargando categorías...')
            const response = await api.get('/categories')
            console.log('✅ Categorías cargadas:', response.data.categories?.length || response.data.length)
            return response.data
        } catch (error) {
            console.error('❌ Error cargando categorías:', error.response?.status)
            throw error
        }
    }
}