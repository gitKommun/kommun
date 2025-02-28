<template>
  <div class="p-4 bg-white shadow-lg rounded-lg mt-24">
    <h2 class="text-xl font-bold mb-4">
      DOT/EUR
    </h2>

    <div v-if="loading" class="text-gray-500">Cargando datos...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>

    <table v-else class="w-full border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="border p-2">Fecha</th>
          <th class="border p-2">Precio de Cierre</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) in closingPrices"
          :key="index"
          class="border-b"
        >
          <td class="border p-2">{{ item.date }}</td>
          <td class="border p-1 font-semibold">{{ item.price }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import Guests from '/src/layouts/Guests.vue';
    defineOptions({
        name: 'Blog',
        layout: Guests,
    });
  const closingPrices = ref([]);
const loading = ref(true);
const error = ref(null);
const currency = ref("EUR"); // Moneda seleccionada (se puede cambiar)

const startDate = new Date("2024-01-01").getTime();
const endDate = new Date("2024-12-31").getTime();

const fetchClosingPrices = async () => {
    loading.value = true;
    error.value = null;
    closingPrices.value = [];

    try {
        const response = await fetch(`https://api.binance.com/api/v3/klines?symbol=BNB${currency.value}&interval=1d&limit=500`);
        const data = await response.json();

        // Filtrar solo los datos en el rango de fechas
        closingPrices.value = data
            .map(candle => ({
                date: new Date(candle[0]), // Fecha en formato Date
                price: parseFloat(candle[4]).toFixed(2).replace('.',',') //+ ` ${currency.value}` // Precio de cierre
            }))
            .filter(entry => entry.date.getTime() >= startDate && entry.date.getTime() <= endDate)
            .map(entry => ({
                date: entry.date.toLocaleDateString(),
                price: entry.price
            }));

    } catch (err) {
        error.value = "Error al obtener los datos";
        console.error(err);
    } finally {
        loading.value = false;
    }
}
// Cargar datos al iniciar
onMounted(fetchClosingPrices);

// Reactivar la consulta si cambia la moneda
watch(currency, fetchClosingPrices);


// Calcular precio medio
const averagePrice = computed(() => {
  //if (closingPrices.value.length === 0) return "N/A";
  const sum = closingPrices.value.reduce((acc, item) => acc + item.price, 0);
  return (sum / closingPrices.value.length).toFixed(4) + ` ${currency.value}`;
});

</script>
