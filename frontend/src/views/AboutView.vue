<template>
  <div class="about-view">
    <div class="container">
      <div class="about-content">
        <h1>Sobre Nosotros</h1>
        <div class="about-section">
          <h2>Nuestra Misión</h2>
          <p>Somos una granja comprometida con la producción de alimentos frescos y saludables para nuestra comunidad.</p>
        </div>
        
        <div class="about-section">
          <h2>Nuestra Historia</h2>
          <p>Con más de 10 años de experiencia, nos dedicamos a la agricultura sostenible y responsable.</p>
        </div>
        
        <div class="about-section">
          <h2>Valores</h2>
          <ul>
            <li>Calidad garantizada</li>
            <li>Sostenibilidad ambiental</li>
    <li>Comercio justo</li>
            <li>Fresco y natural</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style scoped>
.about-view {
  padding: 2rem 0;
  min-height: 70vh;
}

.about-content {
  max-width: 800px;
  margin: 0 auto;
}

.about-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.about-section h2 {
  color: var(--primary-green);
  margin-bottom: 1rem;
}

.about-section p {
  line-height: 1.6;
  color: var(--dark-gray);
}

.about-section ul {
  list-style-type: none;
  padding-left: 0;
}

.about-section li {
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--light-gray);
}

.about-section li:before {
  content: "✓ ";
  color: var(--primary-green);
  font-weight: bold;
}
</style>