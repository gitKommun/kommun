/**
 * Utilidades para el manejo de fechas y tiempos
 */

/**
 * Convierte un objeto Date a formato "HH:mm"
 * @param {Date} date - Objeto fecha
 * @returns {string} Ejemplo: "08:30"
 */
export const formatTimeToString = (date) => {
    if (!date) return '';
    return date.toTimeString().split(' ')[0].substring(0, 5);
};

/**
 * Obtiene la hora de inicio predeterminada (8:00)
 * @returns {Date} Ejemplo: Date object set to current date at 08:00:00
 */
export const defaultStartTime = () => {
    const date = new Date();
    date.setHours(8, 0, 0);
    return date;
};

/**
 * Obtiene la hora de fin predeterminada (22:00)
 * @returns {Date} Ejemplo: Date object set to current date at 22:00:00
 */
export const defaultEndTime = () => {
    const date = new Date();
    date.setHours(22, 0, 0);
    return date;
};

/**
 * Formatea una fecha a string en formato local
 * @param {Date|string} date - Fecha a formatear
 * @returns {string} Ejemplo para España: "25/03/2024"
 */
export const formatDate = (date) => {
    if (!date) return '';
    return new Date(date).toLocaleDateString();
};

/**
 * Formatea fecha y hora
 * @param {Date|string} dateTime - Fecha y hora a formatear
 * @returns {string} Ejemplo para España: "25/03/2024 08:30"
 */
export const formatDateTime = (dateTime) => {
    if (!dateTime) return '';
    const date = new Date(dateTime);
    return `${date.toLocaleDateString()} ${formatTimeToString(date)}`;
}; 