<template>
  <div class="not-found">
    <div class="container">
      <div class="not-found-content">
        <div class="error-illustration">
          <div class="error-icon">🔍</div>
          <div class="error-animation">
            <span>4</span>
            <span class="zero">0</span>
            <span>4</span>
          </div>
        </div>
        
        <div class="error-message">
          <h1>¡Ups! Página no encontrada</h1>
          <p>La página que estás buscando no existe o ha sido movida.</p>
        </div>

        <div class="suggestions">
          <h3>Tal vez quisiste decir:</h3>
          <div class="suggestion-links">
            <router-link to="/" class="suggestion-link">
              <span class="link-icon">🏠</span>
              <span class="link-text">Página de Inicio</span>
            </router-link>
            
            <router-link to="/products" class="suggestion-link">
              <span class="link-icon">🛍️</span>
              <span class="link-text">Nuestros Productos</span>
            </router-link>
            
            <router-link to="/cart" class="suggestion-link">
              <span class="link-icon">🛒</span>
              <span class="link-text">Mi Carrito</span>
            </router-link>
            
            <router-link to="/contact" class="suggestion-link">
              <span class="link-icon">📞</span>
              <span class="link-text">Contacto</span>
            </router-link>
          </div>
        </div>

        <div class="actions">
          <router-link to="/" class="btn btn-primary btn-large">
            <span class="btn-icon">←</span>
            Volver al Inicio
          </router-link>
          
          <button @click="$router.go(-1)" class="btn btn-secondary">
            <span class="btn-icon">↩️</span>
            Regresar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.not-found-content {
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.error-illustration {
  margin-bottom: 2rem;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.8;
}

.error-animation {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.error-animation span {
  font-size: 5rem;
  font-weight: 900;
  color: #2c3e50;
  animation: bounce 2s infinite;
}

.error-animation .zero {
  color: #e74c3c;
  animation-delay: 0.1s;
}

.error-animation span:nth-child(3) {
  animation-delay: 0.2s;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.error-message h1 {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.error-message p {
  color: #7f8c8d;
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.suggestions {
  margin: 2rem 0;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.suggestions h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}

.suggestion-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.suggestion-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  text-decoration: none;
  color: #2c3e50;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.suggestion-link:hover {
  border-color: #3498db;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.link-icon {
  font-size: 1.5rem;
}

.link-text {
  font-weight: 600;
  font-size: 0.9rem;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #27ae60, #219a52);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
  transform: translateY(-2px);
}

.btn-large {
  padding: 1.25rem 2.5rem;
  font-size: 1.1rem;
}

.btn-icon {
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .not-found-content {
    padding: 2rem 1rem;
  }
  
  .error-animation span {
    font-size: 3.5rem;
  }
  
  .error-message h1 {
    font-size: 1.5rem;
  }
  
  .suggestion-links {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>