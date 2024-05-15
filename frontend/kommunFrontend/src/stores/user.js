import { defineStore } from 'pinia'

export const useUserInfo = defineStore("userInfo", {
    //state
    state: () => ({
        userId: null,
        communityId:null,
        name: 'default name',
        surname: 'surname',
        mail:'demo@demo.es'
    }),
    //getters
    //actions
    actions: {
        // save() {
        //     //ref con this.
        // }
    }
})