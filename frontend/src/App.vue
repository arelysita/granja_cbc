// Archivo creado automáticamente
<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import Navbar from './components/common/Navbar.vue'
import Footer from './components/common/Footer.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer
  }
}
</script>

<style>
.main-content {
  min-height: calc(100vh - 120px);
  padding-top: 80px;
}
</style>