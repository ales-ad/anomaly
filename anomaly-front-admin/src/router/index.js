import { createRouter, createWebHistory } from 'vue-router'
import main from '../layout/main.vue'
import useAuthStore from '@/store/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: main,
    redirect: '/events',
    props: true,
    meta: {
      requiredAuth: true,
    },
    children: [
      {
        path: '/users',
        name: 'users',
        component: () => import('../components/users/list.vue'),
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: '/events',
        name: 'events',
        component: () => import('../components/events/list.vue'),
        meta: {
          requiredAuth: true,
        },
      },
      {
        path: '/event/:idEvent',
        name: 'eventsOne',
        props: true,
        component: () => import('../components/events/one.vue'),
        meta: {
          requiredAuth: true,
        },
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "about" */ '../components/login.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.matched.some(record => record.meta.requiredAuth)) {
    if (auth.logined == false) {
      next({
        path: '/login',
      })
    } else {
      next()
    }
  } else {
    if (to.name == 'login') {
      if (auth.logined == true) {
        next({
          path: '/',
        })
      } else {
        next()
      }
    } else {
      next()
    }
  }
})
export default router
