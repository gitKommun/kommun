<template>
  <div class="h-full w-full px-4">
    <div class="border border-slate-200 rounded-2xl p-3 mb-3">
      <div class="flex flex-col md:flex-row gap-y-3 md:gap-y-0 md:gap-x-3 mb-4">
        <!-- <div
          class="w-full flex md:flex-col justify-between md:justify-center items-center bg-slate-100 rounded-xl p-3"
        >
          <span class="uppercase text-xs md:mb-2">Registrados</span>
          <span class="font-bold text-lg">{{ providers.length }}</span>
        </div>
        <div
          class="w-full flex md:flex-col justify-between md:justify-center items-center bg-slate-100 rounded-xl p-3"
        >
          <span class="uppercase text-xs md:mb-2">Favoritos</span>
          <span class="font-bold text-lg">{{ favorites.length }}</span>
        </div> -->
      </div>
      <div class="py-3">
        <MeterGroup :value="providerStats" class="text-sm"/>
      </div>
    </div>
    <DataTable
      :value="providers"
      paginator
      scrollHeight="700px"
      scrollable
      :rows="20"
      :rowsPerPageOptions="[20, 40, 60, 100]"
      tableStyle="min-width: 50rem"
      class="text-xs"
    >
      <Column field="company_name" header="Empresa">
        <template #body="slotProps">
          <span class="flex items-center gap-x-2">
            <span
              :class="`size-8 min-w-8 rounded-lg flex items-center justify-center bg-${
                PROVIDER_COLOR[slotProps.data.type]
              }-100`"
            >
              <component
                :is="PROVIDER_ICONS[slotProps.data.type]"
                :class="`scale-75 text-${
                  PROVIDER_COLOR[slotProps.data.type]
                }-500`"
              />
            </span>
            <span class="">{{
              slotProps.data.company_name
            }}</span>
          </span>
        </template>
      </Column>
      <Column field="phone" header="Teléfono"></Column>
      <Column field="email" header="Correo electrónico"></Column>
      <Column field="address" header="Dirección"></Column>
      <Column field="rating" header="Valoración" sortable>
        <template #body="slotProps">
          <Rating
            :modelValue="slotProps.data.rating"
            :readonly="true"
            :cancel="false"
            :cancelTooltip="false"
          />
        </template>
      </Column>
      <Column field="contact_person" header="Contacto"></Column>
    </DataTable>
  </div>
</template>
<script setup>
import { ref, computed, shallowRef } from "vue";
import Main from "/src/layouts/Main.vue";
import { PROVIDER_COLOR, PROVIDER_HEX } from "/src/constants/colors.js";
import { PROVIDER_LABEL } from "/src/constants/labels.js";
import IconBolt from "@/components/icons/IconBolt.vue";
import IconDroplet from "@/components/icons/IconDroplet.vue";
import IconLockSquareRounded from "@/components/icons/IconLockSquareRounded.vue";
import IconWall from "@/components/icons/IconWall.vue";
import IconElevator from "@/components/icons/IconElevator.vue";
import IconWindow from "@/components/icons/IconWindow.vue";
import IconPlant from "@/components/icons/IconPlant.vue";
import IconApiApp from "@/components/icons/IconApiApp.vue";
import IconAntenna from "@/components/icons/IconAntenna.vue";
import IconShieldCheck from "@/components/icons/IconShieldCheck.vue";
import IconShieldStar from "@/components/icons/IconShieldStar.vue";
import IconScale from "@/components/icons/IconScale.vue";
import IconPaint from "@/components/icons/IconPaint.vue";
import IconBucketDroplet from "@/components/icons/IconBucketDroplet.vue";

defineOptions({
  name: "Providers",
  layout: Main,
});

const PROVIDER_ICONS = {
  electricity: IconBolt,
  plumbing: IconDroplet,
  locksmiths: IconLockSquareRounded,
  painters: IconPaint,
  antenna_technicians: IconAntenna,
  bricklayers: IconWall,
  elevators: IconElevator,
  glaziers: IconWindow,
  cleaning: IconBucketDroplet,
  gardening: IconPlant,
  security: IconShieldStar,
  insurance: IconShieldCheck,
  lawyers: IconScale,
  others: IconApiApp,
};
const providers = ref([
  {
    company_name: "LockGuard Solutions",
    phone: "(321) 654-9870",
    email: "info@lockguard.com",
    address: "123 Maple St, Miami, FL",
    type: "electricity",
    rating: 4,
    contact_person: "Carlos Jiménez",
    contact_person_email: "carlos@lockguard.com",
    contact_person_phone: "(321) 654-9871",
  },
  {
    company_name: "Green Plumbing Experts",
    phone: "(415) 789-6543",
    email: "contact@greenplumbers.com",
    address: "456 Oak St, San Francisco, CA",
    type: "plumbing",
    rating: 3,
    contact_person: "Lucía Gómez",
    contact_person_email: "lucia@greenplumbers.com",
    contact_person_phone: "(415) 789-6544",
  },
  {
    company_name: "Bright Painters Inc.",
    phone: "(212) 555-9012",
    email: "info@brightpainters.com",
    address: "789 Elm St, New York, NY",
    type: "painters",
    rating: 1,
    contact_person: "Miguel Torres",
    contact_person_email: "miguel@brightpainters.com",
    contact_person_phone: "(212) 555-9013",
  },
  {
    company_name: "Skyline Antenna Services",
    phone: "(305) 876-4321",
    email: "support@skylineantenna.com",
    address: "102 Cedar St, Miami, FL",
    type: "antenna_technicians",
    rating: 5,
    contact_person: "Ana López",
    contact_person_email: "ana@skylineantenna.com",
    contact_person_phone: "(305) 876-4322",
  },
  {
    company_name: "BrickMaster Constructions",
    phone: "(702) 345-6789",
    email: "contact@brickmaster.com",
    address: "231 Pine St, Las Vegas, NV",
    type: "bricklayers",
    rating: 4,
    contact_person: "Ricardo Fernández",
    contact_person_email: "ricardo@brickmaster.com",
    contact_person_phone: "(702) 345-6790",
  },
  {
    company_name: "HighRise Elevators",
    phone: "(818) 222-3333",
    email: "info@highriseelevators.com",
    address: "456 Birch St, Los Angeles, CA",
    type: "elevators",
    rating: 2,
    contact_person: "Sofía Morales",
    contact_person_email: "sofia@highriseelevators.com",
    contact_person_phone: "(818) 222-3334",
  },
  {
    company_name: "Crystal Clear Windows",
    phone: "(303) 555-8765",
    email: "hello@crystalclear.com",
    address: "678 Aspen St, Denver, CO",
    type: "electricity",
    rating: 3,
    contact_person: "Tomás Herrera",
    contact_person_email: "tomas@crystalclear.com",
    contact_person_phone: "(303) 555-8766",
  },
  {
    company_name: "Shiny Cleaners",
    phone: "(212) 111-2222",
    email: "service@shinycleaners.com",
    address: "987 Palm St, New York, NY",
    type: "cleaning",
    rating: 4,
    contact_person: "Isabel Ramírez",
    contact_person_email: "isabel@shinycleaners.com",
    contact_person_phone: "(212) 111-2223",
  },
  {
    company_name: "EcoGardens Landscaping",
    phone: "(619) 444-5678",
    email: "support@ecogardens.com",
    address: "321 Spruce St, San Diego, CA",
    type: "gardening",
    rating: 5,
    contact_person: "Daniel Pérez",
    contact_person_email: "daniel@ecogardens.com",
    contact_person_phone: "(619) 444-5679",
  },
  {
    company_name: "SecureWatch Security",
    phone: "(512) 999-8888",
    email: "info@securewatch.com",
    address: "555 Redwood St, Austin, TX",
    type: "security",
    rating: 1,
    contact_person: "Paula Ortega",
    contact_person_email: "paula@securewatch.com",
    contact_person_phone: "(512) 999-8889",
  },
  {
    company_name: "SafeHome Insurance",
    phone: "(305) 777-7777",
    email: "contact@safehome.com",
    address: "678 Sequoia St, Miami, FL",
    type: "insurance",
    rating: 4,
    contact_person: "Alberto Núñez",
    contact_person_email: "alberto@safehome.com",
    contact_person_phone: "(305) 777-7778",
  },
  {
    company_name: "LexTrust Legal Services",
    phone: "(650) 888-1234",
    email: "support@lextrust.com",
    address: "890 Walnut St, San Jose, CA",
    type: "lawyers",
    rating: 2,
    contact_person: "Elena Sánchez",
    contact_person_email: "elena@lextrust.com",
    contact_person_phone: "(650) 888-1235",
  },
  {
    company_name: "FixIt All Services",
    phone: "(818) 555-9090",
    email: "service@fixitall.com",
    address: "432 Main St, Los Angeles, CA",
    type: "others",
    rating: 3,
    contact_person: "Jorge Ruiz",
    contact_person_email: "jorge@fixitall.com",
    contact_person_phone: "(818) 555-9091",
  },
  {
    company_name: "LockGuard Solutions",
    phone: "(321) 654-9870",
    email: "info@lockguard.com",
    address: "123 Maple St, Miami, FL",
    type: "locksmiths",
    rating: 2,
    contact_person: "Carlos Jiménez",
    contact_person_email: "carlos@lockguard.com",
    contact_person_phone: "(321) 654-9871",
  },
  {
    company_name: "SecureKey Masters",
    phone: "(555) 123-4567",
    email: "contact@securekey.com",
    address: "987 Oak St, Los Angeles, CA",
    type: "locksmiths",
    rating: 4,
    contact_person: "Fernando López",
    contact_person_email: "fernando@securekey.com",
    contact_person_phone: "(555) 123-4568",
  },
  {
    company_name: "Green Plumbing Experts",
    phone: "(415) 789-6543",
    email: "contact@greenplumbers.com",
    address: "456 Oak St, San Francisco, CA",
    type: "plumbing",
    rating: 5,
    contact_person: "Lucía Gómez",
    contact_person_email: "lucia@greenplumbers.com",
    contact_person_phone: "(415) 789-6544",
  },
  {
    company_name: "AquaFlow Plumbing",
    phone: "(222) 555-9876",
    email: "info@aquaflow.com",
    address: "742 River St, Seattle, WA",
    type: "plumbing",
    rating: 4,
    contact_person: "Javier Pérez",
    contact_person_email: "javier@aquaflow.com",
    contact_person_phone: "(222) 555-9877",
  },
  {
    company_name: "Bright Painters Inc.",
    phone: "(212) 555-9012",
    email: "info@brightpainters.com",
    address: "789 Elm St, New York, NY",
    type: "painters",
    rating: 2,
    contact_person: "Miguel Torres",
    contact_person_email: "miguel@brightpainters.com",
    contact_person_phone: "(212) 555-9013",
  },
  {
    company_name: "Elite Home Painters",
    phone: "(606) 987-6543",
    email: "contact@elitepainters.com",
    address: "123 Brush St, Austin, TX",
    type: "painters",
    rating: 4,
    contact_person: "Esteban Morales",
    contact_person_email: "esteban@elitepainters.com",
    contact_person_phone: "(606) 987-6544",
  },
  {
    company_name: "Skyline Antenna Services",
    phone: "(305) 876-4321",
    email: "support@skylineantenna.com",
    address: "102 Cedar St, Miami, FL",
    type: "antenna_technicians",
    rating: 3,
    contact_person: "Ana López",
    contact_person_email: "ana@skylineantenna.com",
    contact_person_phone: "(305) 876-4322",
  },
  {
    company_name: "SignalBoost Antennas",
    phone: "(808) 654-3210",
    email: "info@signalboost.com",
    address: "567 Satellite St, Denver, CO",
    type: "antenna_technicians",
    rating: 5,
    contact_person: "Pedro Hernández",
    contact_person_email: "pedro@signalboost.com",
    contact_person_phone: "(808) 654-3211",
  },
  {
    company_name: "BrickMaster Constructions",
    phone: "(702) 345-6789",
    email: "contact@brickmaster.com",
    address: "231 Pine St, Las Vegas, NV",
    type: "bricklayers",
    rating: 4,
    contact_person: "Ricardo Fernández",
    contact_person_email: "ricardo@brickmaster.com",
    contact_person_phone: "(702) 345-6790",
  },
  {
    company_name: "SolidBuild Bricklayers",
    phone: "(999) 123-4567",
    email: "info@solidbuild.com",
    address: "345 Mason St, Chicago, IL",
    type: "bricklayers",
    rating: 1,
    contact_person: "Luis Ortega",
    contact_person_email: "luis@solidbuild.com",
    contact_person_phone: "(999) 123-4568",
  },
  {
    company_name: "HighRise Elevators",
    phone: "(818) 222-3333",
    email: "info@highriseelevators.com",
    address: "456 Birch St, Los Angeles, CA",
    type: "elevators",
    rating: 3,
    contact_person: "Sofía Morales",
    contact_person_email: "sofia@highriseelevators.com",
    contact_person_phone: "(818) 222-3334",
  },
  {
    company_name: "Ascend Elevator Services",
    phone: "(707) 654-3212",
    email: "contact@ascendelevators.com",
    address: "789 Lift St, Houston, TX",
    type: "elevators",
    rating: 4,
    contact_person: "Daniela Castro",
    contact_person_email: "daniela@ascendelevators.com",
    contact_person_phone: "(707) 654-3213",
  },
  {
    company_name: "Crystal Clear Windows",
    phone: "(303) 555-8765",
    email: "hello@crystalclear.com",
    address: "678 Aspen St, Denver, CO",
    type: "glaziers",
    rating: 2,
    contact_person: "Tomás Herrera",
    contact_person_email: "tomas@crystalclear.com",
    contact_person_phone: "(303) 555-8766",
  }
]);

const providerStats = computed(() => {

    const total = providers.value.length;
    if (total === 0) return [];
    const typeCounts = {};

    // Contar ocurrencias de cada type
    providers.value.forEach(({ type }) => {
      typeCounts[type] = (typeCounts[type] || 0) + 1;
    });

    // Convertir a array con porcentajes
    return Object.entries(typeCounts).map(([type, count]) => ({
      label: PROVIDER_LABEL[type],
      color: PROVIDER_HEX[type] || "#000000",
      value: Math.round((count / total) * 100),
    }));

});
</script>
