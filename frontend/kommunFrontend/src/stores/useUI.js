import { defineStore } from 'pinia'

export const useUI = defineStore("UI", {
    // state
    state: () => ({
        communityList: 'card',
    }),
    // getters
    // actions
    actions: {
        setCommunityList(data) { 
            //console.log('store', value.data)
            this.communityList = data;
        },
    }
})