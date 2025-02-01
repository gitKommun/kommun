

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice';
import { createPinia } from 'pinia';
import kommunTheme from './kommunTheme';



import './index.css';
import 'primeicons/primeicons.css'


const pinia = createPinia();
const app = createApp(App);

app.use(pinia);
app.use(router);


//DIRECTIVAS
import Ripple from 'primevue/ripple';
app.directive('ripple', Ripple);
import AnimateOnScroll from 'primevue/animateonscroll';
app.directive('animateonscroll', AnimateOnScroll);

app.use(PrimeVue, {
    ripple:true,
    theme: {
        preset: {
            ...Aura,
            semantic: {
                ...Aura.semantic,
                ...kommunTheme
            }
        },
        options: {
            prefix: 'p',
            darkModeSelector: '',
            cssLayer: false
        }
    }, 
    
});
app.use(ToastService);
app.use(ConfirmationService);




//PRIME COMPONENTS
import Button from "primevue/button"
app.component('Button', Button);

import Dialog from 'primevue/dialog';
app.component('Dialog', Dialog);

import InputText from 'primevue/inputtext';
app.component('InputText', InputText);

import Toast from 'primevue/toast';
app.component('Toast', Toast);

import Checkbox from 'primevue/checkbox';
app.component('Checkbox', Checkbox)

import InputNumber from 'primevue/inputnumber';
app.component('InputNumber', InputNumber)

import ToggleSwitch from 'primevue/toggleswitch';
app.component('ToggleSwitch',ToggleSwitch)

import Select from 'primevue/select';
app.component('Select', Select)

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';  
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)
app.component('Row', Row)

import Tag from 'primevue/tag';
app.component('Tag', Tag)

import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
app.component('InputGroup', InputGroup)
app.component('InputGroupAddon', InputGroupAddon)

import Password from 'primevue/password';
app.component('Password', Password)

import Avatar from 'primevue/avatar';
import AvatarGroup from 'primevue/avatargroup';
app.component('Avatar', Avatar)
app.component('AvatarGroup', AvatarGroup)


import Textarea from 'primevue/textarea';
app.component('Textarea', Textarea)

import Stepper from 'primevue/stepper';
import StepList from 'primevue/steplist';
import StepPanels from 'primevue/steppanels';
import StepItem from 'primevue/stepitem';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';
app.component('Stepper', Stepper)
app.component('StepList', StepList)
app.component('StepPanels', StepPanels)
app.component('StepItem', StepItem)
app.component('Step', Step)
app.component('StepPanel', StepPanel)

import DatePicker from 'primevue/datepicker';
app.component('DatePicker', DatePicker)

import Popover from 'primevue/popover';
app.component('Popover', Popover)


import MultiSelect from 'primevue/multiselect';
app.component('MultiSelect', MultiSelect)

import Card from 'primevue/Card';
app.component('Card', Card)

import Fieldset from 'primevue/Fieldset';
app.component('Fieldset', Fieldset)

import ProgressBar from 'primevue/ProgressBar';
app.component('ProgressBar', ProgressBar)


import SelectButton from 'primevue/selectbutton';
app.component('SelectButton', SelectButton)

import ConfirmDialog from 'primevue/confirmdialog';
app.component('ConfirmDialog', ConfirmDialog)

import MeterGroup from 'primevue/metergroup';
app.component('MeterGroup', MeterGroup)


import Tabs from "primevue/tabs";
import TabList from "primevue/tablist";
import Tab from "primevue/tab";
import TabPanels from "primevue/tabpanels";
import TabPanel from "primevue/tabpanel";
app.component('Tabs', Tabs)
app.component('TabList', TabList)
app.component('Tab', Tab)
app.component('TabPanels', TabPanels)
app.component('TabPanel', TabPanel)

import Rating from "primevue/rating";
app.component('Rating', Rating)


app.mount('#app');
