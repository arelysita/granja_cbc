// frontend/src/services/paymentService.js
import api from './api';

const paymentService = {

    /**
     * Obtener métodos de pago disponibles
     */
    async getPaymentMethods() {
        try {
            const response = await api.get('/pagos/metodos');
            return response.data;
        } catch (error) {
            console.error("Error obteniendo métodos de pago:", error);
            throw error;
        }
    },

    /**
     * Procesar un pago
     */
    async processPayment(paymentData) {
        try {
            const response = await api.post('/pagos/procesar', paymentData);
            return response.data;
        } catch (error) {
            console.error("Error procesando pago:", error);
            throw error;
        }
    },

    /**
     * Obtener historial de pagos del usuario
     */
    async getPaymentHistory() {
        try {
            const response = await api.get('/pagos/historial');
            return response.data;
        } catch (error) {
            console.error("Error obteniendo historial de pagos:", error);
            throw error;
        }
    }
};

export default paymentService;