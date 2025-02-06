<template>
    <div
        ref="container"
        class="flex h-full w-full items-center justify-center"
    />
</template>

<script setup>
    import { ref, computed, watch, useTemplateRef, onMounted } from 'vue';

    import Highcharts from 'highcharts';

    defineOptions({
        name: 'HighChart',
    });

    const props = defineProps({
        type: {
            type: String,
            default: 'column',
        },
        options: {
            type: Object,
            default: () => ({}),
        },
    });

    const container = useTemplateRef('container');
    const chart = ref(null);

    const localOptions = computed(() => {
        return {
            chart: {
                type: props.type,
                // backgroundColor: 'transparent',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                backgroundColor: 'rgba(255,255,255,0)',
            },
            title: false,
            credits: {
                enabled: false,
            },
            ...props.options,
        };
    });

    onMounted(() => {
        createChart();
    });

    watch(
        () => props.options,
        () => {
            createChart();
        },
    );

    const createChart = () => {
        chart.value = Highcharts.chart(container.value, {
            ...localOptions.value,
        });
    };
</script>
