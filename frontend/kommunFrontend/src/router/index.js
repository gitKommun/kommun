import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes.js';

import { useUserStore } from '/src/stores/useUserStore.js';
import { useHttp } from '/src/composables/useHttp.js'; 
import { getCookie, removeCookie } from '/src/utils/cookies.js';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes({ authGuard, guestGuard }),
});

export default router;

router.beforeEach(async (to, from, next) => {
  // user store
  const {
    user,
    setUser,
  } = useUserStore();
  
  const http = useHttp();
  const token = getCookie('csrftoken');
  
  if (token && !user) {
    try {
      const me = await http.get(`members/me/`);
      setUser(me);
    } catch (error) {
      removeCookie('csrftoken');
      removeCookie('sessionid');
    }
	}

  next();
})


function beforeEnter(routes, callback) {
	return routes.map(route => {
		return { ...route, beforeEnter: callback }
	});
}

function authGuard(routes) {
	return beforeEnter(routes, async (to, from, next) => {
		const token = getCookie('csrftoken');

		if (!token) {
      return next({ name: 'login' });
		}

		next();
	});
}

function guestGuard(routes) {
  return beforeEnter(routes, async (to, from, next) => {
    const token = getCookie('csrftoken');

    if (token) {
      return next({ name: 'properties' });
    }

    next();
  });
}
