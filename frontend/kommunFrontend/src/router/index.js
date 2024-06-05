import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes.js';
import { getCookie } from '/src/utils/cookies.js';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes({ authGuard, guestGuard }),
});

export default router;

router.beforeEach(async (to, from, next) => {
  // const token = getCookie('csrftoken');
  
	// if (token && !user) {
	// 	await getAuthUser(next)
	// }

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
