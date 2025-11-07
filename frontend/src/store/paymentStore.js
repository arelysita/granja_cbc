// frontend/src/store/paymentStore.js
import { defineStore } from 'pinia';
import paymentService from '../services/paymentService';

export const usePaymentStore = defineStore('payment', {
    state: () => ({
        paymentMethods: [],
        paymentHistory: [],
        currentPayment: null,
        isLoading: false,
        error: null,
    }),

    getters: {
        activePaymentMethods: (state) => state.paymentMethods.filter(method => method.activo),
        digitalWallets: (state) => state.paymentMethods.filter(method => method.tipo_billetera),
        bankTransfers: (state) => state.paymentMethods.filter(method => 
            method.codigo === 'pse' || method.codigo === 'transferencia_bancaria'
        ),
        cashMethods: (state) => state.paymentMethods.filter(method => 
            method.codigo === 'efecty' || method.codigo === 'baloto' || method.codigo === 'contraentrega'
        ),
    },

    actions: {
        /**
         * Cargar métodos de pago disponibles
         */
        async fetchPaymentMethods() {
            this.isLoading = true;
            this.error = null;
            try {
                const data = await paymentService.getPaymentMethods();
                this.paymentMethods = data.metodos_pago;
            } catch (error) {
                this.error = error;
                console.error('Error cargando métodos de pago:', error);
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Procesar un pago
         */
        async processPayment(paymentData) {
            this.isLoading = true;
            this.error = null;
            try {
                const data = await paymentService.processPayment(paymentData);
                this.currentPayment = data.pago;
                return data;
            } catch (error) {
                this.error = error;
                console.error('Error procesando pago:', error);
                throw error;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Cargar historial de pagos
         */
        async fetchPaymentHistory() {
            this.isLoading = true;
            this.error = null;
            try {
                const data = await paymentService.getPaymentHistory();
                this.paymentHistory = data.pagos;
            } catch (error) {
                this.error = error;
                console.error('Error cargando historial de pagos:', error);
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * Limpiar estado actual
         */
        clearCurrentPayment() {
            this.currentPayment = null;
            this.error = null;
        }
    }
});