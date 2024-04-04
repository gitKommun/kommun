<template>
  <div class="h-full w-full">
    <div class="text-slate-950 text-3xl font-bold truncate pl-4 md:pl-16 py-6 flex flex-col">
      {{title}}
      <span class="text-sm text-slate-500 font-medium">Comunidad "Las Veredillas"</span>
    </div>
    <div class="w-full p-4 flex justify-end">
      <vs-button color="dark">Añadir miembros</vs-button>
    </div>
    <div class="px-4">
        <!-- <div ref="table"></div> -->
        <vs-table>
            <template #thead>
              <vs-tr>
                <vs-th>  </vs-th>
                <vs-th> Name </vs-th>
                <vs-th> Email </vs-th>
                <vs-th> Phone </vs-th>
                <vs-th> Coefficent </vs-th>
                <vs-th> Stair </vs-th>
                <vs-th> Floor </vs-th>
                <vs-th> Number </vs-th>
                <vs-th> Letter </vs-th>
                <vs-th> Payments </vs-th>
              </vs-tr>
            </template>
            <template #tbody>
            <vs-tr v-for="(tr, i) in users" :key="i" :data="tr">
              <vs-td>
                <vs-avatar>
                  <img :src="'public/'+tr.avatar" alt="" />
                </vs-avatar>
              </vs-td>
              <vs-td>
                {{ tr.name }}
              </vs-td>
              <vs-td>
                {{ tr.email }}
              </vs-td>
              <vs-td>
                {{ tr.phone }}
              </vs-td>
              <vs-td>
                {{ tr.rate }}
              </vs-td>
              <vs-td>
                {{ tr.stair}}
              </vs-td>
              <vs-td>
                {{ tr.floor }}
              </vs-td>
              <vs-td>
                {{ tr.number }}
              </vs-td>
              <vs-td>
                {{ tr.letter}}
              </vs-td>
              <vs-td>
                {{ tr.credit }}
              </vs-td>
              
            </vs-tr>
      </template>
        </vs-table>
    </div>
    
  </div>  
</template>
<script setup>
import { ref , shallowRef, reactive, onMounted} from 'vue'
import Main from '/src/layouts/Main.vue';

defineOptions({
  name: 'members',
  layout: Main
})
const title = ref('Miembros')
const users = ref([
   { 
    id: 1,
      avatar:'avatar_3.png',
        name: 'John Doe',
        email: 'john@example.com',
        phone: '123-456-7890',
        rate: 4.5,
        floor: 3,
        stair: 'A',
        number: 12,
        letter: 'B',
        credit: 1000
    },
  { 
    id: 2,
      avatar:'avatar_4.png',
        name: 'Alice Smith',
        email: 'alice@example.com',
        phone: '987-654-3210',
        rate: 3.8,
        floor: 2,
        stair: 'B',
        number: 7,
        letter: 'C',
        credit: 1500
    },
  { 
    id: 3,
      avatar:'avatar_5.png',
        name: 'Bob Johnson',
        email: 'bob@example.com',
        phone: '555-555-5555',
        rate: 4.2,
        floor: 5,
        stair: 'C',
        number: 23,
        letter: 'A',
        credit: 2000
    }
]); //data for table to display

 // users.value =

</script>

