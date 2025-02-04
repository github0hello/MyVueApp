import { createRouter, createWebHistory } from 'vue-router'
import Index_pages from '../views/index_pages.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index_pages,
    },
    {
      path:'/ComfyUI/runner',
      name:'ComfyUI',
      component:()=>import('../views/ComfyUI/ComfyUI_runner.vue')

    },
    {
      path:'/settings',
      name:'settings',
      component:()=>import('../views/Setting_page.vue')
    }
  ],
})

export default router
