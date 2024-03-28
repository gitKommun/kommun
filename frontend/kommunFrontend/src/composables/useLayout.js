import { shallowRef, watch } from 'vue';
import { useRoute } from 'vue-router';

const layout = shallowRef('div');

export function useLayout(defaultLayout = 'div') {
    const route = useRoute();

    watch(
        () => route?.name,
        () => layout.value = route?.matched[0].components?.default?.layout || defaultLayout
    );

    return layout;
};