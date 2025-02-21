export default function routes({ authGuard, guestGuard }) {
    return [
      ...guestGuard([
        {
          path: "/",
          name: "Landing",
          component: () => import("../views/Landing.vue"),
        },
        {
          path: "/pricing",
          name: "pricing",
          component: () => import("../views/Pricing.vue"),
        },
        {
          path: "/contact",
          name: "contact",
          component: () => import("../views/Contact.vue"),
        },
        {
          path: "/login",
          name: "login",
          component: () => import("../views/auth/Login.vue"),
        },
        {
          path: "/register",
          name: "register",
          component: () => import("../views/auth/Register.vue"),
        },
        {
          path: "/recovery",
          name: "recovery",
          component: () => import("../views/auth/Recovery.vue"),
        },
        {
          path: "/provider_performance/:id",
          name: "provider_performance",
          component: () => import("../views/ProviderPerformance.vue"),
        },
      ]),
      ...authGuard([
        {
          path: "/properties",
          name: "properties",
          component: () => import("../views/admin/Properties.vue"),
        },
        {
          path: "/communities",
          name: "communities",
          component: () => import("../views/admin/Communities.vue"),
        },
        {
          path: "/owners",
          name: "owners",
          component: () => import("../views/admin/Owners.vue"),
        },
        {
          path: "/documents",
          name: "documents",
          component: () => import("../views/admin/Documents.vue"),
        },
        {
          path: "/incidences",
          name: "incidences",
          component: () => import("../views/admin/Incidences.vue"),
        },
        {
          path: "/surveys",
          name: "surveys",
          component: () => import("../views/admin/Surveys.vue"),
        },
        {
          path: "/finance",
          name: "finance",
          component: () => import("../views/admin/Finance.vue"),
        },
        {
          path: "/communication",
          name: "communication",
          component: () => import("../views/admin/Communication.vue"),
        },
        {
          path: "/zones",
          name: "zones",
          component: () => import("../views/admin/Zones.vue"),
        },
        {
          path: "/providers",
          name: "providers",
          component: () => import("../views/admin/Providers.vue"),
        },
        {
          path: "/community_settings/:id",
          name: "community_settings",
          component: () => import("../views/admin/CommunitySettings.vue"),
        },
        {
          path: "/account",
          name: "account",
          component: () => import("../views/admin/Account.vue"),
        },
        {
          path: "/onboarding",
          name: "onboarding",
          component: () => import("../views/admin/Onboarding.vue"),
        },
        {
          path: "/profile",
          name: "profile",
          component: () => import("../views/admin/Profile.vue"),
        },
        {
          path: "/:pathMatch(.*)*",
          name: "404",
          component: () => import("../views/admin/404.vue"),
        },
      ]),

      // {
      //   path: '/about',
      //   name: 'about',
      //   // route level code-splitting
      //   // this generates a separate chunk (About.[hash].js) for this route
      //   // which is lazy-loaded when the route is visited.
      //   component: () => import('../views/AboutView.vue')
      // }
    ];
}