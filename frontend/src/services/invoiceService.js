// frontend/src/services/invoiceService.js
import api from './api';

const invoiceService = {

    /**
     * Obtener factura de una venta
     */
    async getInvoiceBySale(saleId) {
        try {
            const response = await api.get(`/facturas/venta/${saleId}`);
            return response.data;
        } catch (error) {
            console.error("Error obteniendo factura:", error);
            throw error;
        }
    },

    /**
     * Obtener facturas del usuario
     */
    async getUserInvoices() {
        try {
            const response = await api.get('/facturas/usuario');
            return response.data;
        } catch (error) {
            console.error("Error obteniendo facturas:", error);
            throw error;
        }
    },

    /**
     * Descargar factura en PDF
     */
    async downloadInvoice(invoiceId) {
        try {
            const response = await api.get(`/facturas/descargar/${invoiceId}`, {
                responseType: 'blob'
            });
            return response.data;
        } catch (error) {
            console.error("Error descargando factura:", error);
            throw error;
        }
    }
};

export default invoiceService;