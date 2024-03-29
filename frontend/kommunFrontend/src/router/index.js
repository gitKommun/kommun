import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Features from '../views/Features.vue'
import Login from '../views/auth/Login.vue'
import Recovery from '../views/auth/Recovery.vue'
import Register from '../views/auth/Register.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },{
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
     {
      path: '/recovery',
      name: 'recovery',
      component: Recovery
    },
    {
      path: '/features',
      name: 'features',
      component: Features
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
