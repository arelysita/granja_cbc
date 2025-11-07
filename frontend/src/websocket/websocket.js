class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    // Usar el mismo host de tu API
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = 'localhost:8080'; // o tu host específico
    const wsUrl = `${protocol}//${host}/ws`;
    
    console.log('Conectando WebSocket a:', wsUrl);

    try {
      this.ws = new WebSocket(wsUrl);
      
      this.ws.onopen = () => {
        console.log('✅ WebSocket conectado exitosamente');
        this.reconnectAttempts = 0;
      };
      
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      };
      
      this.ws.onerror = (error) => {
        console.error('❌ Error en WebSocket:', error);
      };
      
      this.ws.onclose = (event) => {
        console.log('🔌 WebSocket desconectado');
        if (!event.wasClean) {
          this.handleReconnection();
        }
      };
      
    } catch (error) {
      console.error('❌ Error al crear WebSocket:', error);
      this.handleReconnection();
    }
  }

  handleMessage(data) {
    // Procesar mensajes según tu aplicación
    console.log('📨 Mensaje WebSocket:', data);
    // Ejemplo: actualizar notificaciones, ventas en tiempo real, etc.
  }

  handleReconnection() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * this.reconnectAttempts;
      
      console.log(`🔄 Reconectando en ${delay}ms (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, delay);
    } else {
      console.error('❌ Máximo de intentos de reconexión alcanzado');
    }
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

export const webSocketService = new WebSocketService();