import { createRouter, createWebHistory } from 'vue-router'
import NotFoundPage from './components/NotFoundPage.vue'

const routes = [
  { path: '/:pathMatch(.*)*', component: NotFoundPage }, // 通配符路由
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
