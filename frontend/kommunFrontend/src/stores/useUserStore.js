import { defineStore } from 'pinia'

export const useUserStore = defineStore("userInfo", {
    // state
    state: () => ({
        user: undefined,
    }),
    // getters
    // actions
    actions: {
        setUser(user) { 
            //console.log('store', user.data)
            this.user = user.data;
        },
    }
})