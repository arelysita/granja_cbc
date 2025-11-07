// Archivo creado automáticamente
<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>🌱 Granja CBC</h3>
          <p>Productos frescos y naturales directamente de nuestra granja a tu mesa.</p>
          <div class="social-links">
            <a href="#" class="social-link">📘</a>
            <a href="#" class="social-link">📷</a>
            <a href="#" class="social-link">🐦</a>
          </div>
        </div>
        
        <div class="footer-section">
          <h4>Enlaces Rápidos</h4>
          <ul>
            <li><router-link to="/">Inicio</router-link></li>
            <li><router-link to="/products">Productos</router-link></li>
            <li><router-link to="/about">Nosotros</router-link></li>
            <li><router-link to="/contact">Contacto</router-link></li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>Contacto</h4>
          <ul>
            <li>📞 +57 1 234 5678</li>
            <li>✉️ info@granjacbc.com</li>
            <li>📍 Bogotá, Colombia</li>
          </ul>
        </div>
        
        <div class="footer-section">
          <h4>Horario de Atención</h4>
          <ul>
            <li>Lunes - Viernes: 8:00 AM - 6:00 PM</li>
            <li>Sábados: 8:00 AM - 2:00 PM</li>
            <li>Domingos: Cerrado</li>
          </ul>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2024 Granja CBC. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background: var(--dark-green);
  color: var(--white);
  padding: 40px 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 40px;
  margin-bottom: 30px;
}

.footer-section h3 {
  color: var(--light-green);
  margin-bottom: 15px;
  font-size: 1.5rem;
}

.footer-section h4 {
  color: var(--light-green);
  margin-bottom: 15px;
}

.footer-section p {
  line-height: 1.6;
  margin-bottom: 20px;
  opacity: 0.9;
}

.footer-section ul {
  list-style: none;
}

.footer-section li {
  margin-bottom: 8px;
  opacity: 0.9;
}

.footer-section a {
  color: var(--white);
  text-decoration: none;
  transition: var(--transition);
}

.footer-section a:hover {
  color: var(--light-green);
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-link {
  display: inline-block;
  padding: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  transition: var(--transition);
}

.social-link:hover {
  background: var(--light-green);
  transform: translateY(-2px);
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 20px;
  text-align: center;
  opacity: 0.8;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
</style>