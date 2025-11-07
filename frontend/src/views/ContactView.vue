<template>
  <div class="contact-view">
    <div class="container"> 
      <div class="contact-content">
        <h1>Contacto</h1>
        
        <div class="contact-grid">
          <div class="contact-info">
            <h2>Información de Contacto</h2>
            
            <div class="contact-item">
              <h3>📍 Dirección</h3>
              <p>Av. Principal #123<br>Ciudad, País</p>
            </div>
            
            <div class="contact-item">
              <h3>📞 Teléfono</h3>
              <p>+1 (555) 123-4567</p>
            </div>
            
            <div class="contact-item">
              <h3>✉️ Email</h3>
              <p>info@granja.com</p>
            </div>
            
            <div class="contact-item">
              <h3>🕒 Horario de Atención</h3>
              <p>Lunes a Viernes: 8:00 - 18:00<br>Sábados: 9:00 - 14:00</p>
            </div>
          </div>
          
          <div class="contact-form">
            <h2>Envíanos un Mensaje</h2>
            <form @submit.prevent="submitForm" class="form">
              <div class="form-group">
                <label for="name">Nombre completo</label>
                <input type="text" id="name" v-model="form.name" required>
              </div>
              
              <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="form.email" required>
              </div>
              
              <div class="form-group">
                <label for="subject">Asunto</label>
                <input type="text" id="subject" v-model="form.subject" required>
              </div>
              
              <div class="form-group">
                <label for="message">Mensaje</label>
                <textarea id="message" v-model="form.message" rows="5" required></textarea>
              </div>
              
              <button type="submit" class="btn btn-primary">Enviar Mensaje</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ContactView',
  setup() {
    const form = ref({
      name: '',
      email: '',
      subject: '',
      message: ''
    })

    const submitForm = () => {
      // Aquí puedes agregar la lógica para enviar el formulario
      console.log('Formulario enviado:', form.value)
      alert('¡Mensaje enviado! Te contactaremos pronto.')
      
      // Resetear formulario
      form.value = {
        name: '',
        email: '',
        subject: '',
        message: ''
      }
    }

    return {
      form,
      submitForm
    }
  }
}
</script>

<style scoped>
.contact-view {
  padding: 2rem 0;
  min-height: 70vh;
}

.contact-content {
  max-width: 1200px;
  margin: 0 auto;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  margin-top: 2rem;
}

.contact-info, .contact-form {
  background: var(--white);
  padding: 2rem;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.contact-item {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--light-gray);
}

.contact-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.contact-item h3 {
  color: var(--primary-green);
  margin-bottom: 0.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: var(--text-dark);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--light-gray);
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-green);
}

.btn {
  width: 100%;
  padding: 0.75rem;
}

/* Responsive */
@media (max-width: 768px) {
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>