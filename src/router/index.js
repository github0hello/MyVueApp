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
    },
    {
      path:"/Dowload_models",
      name:"Dowload models",
      component:()=>import('../views/model_downloader.vue')
    },
    {
      path:"/custom_nodes",
      name:"custom_nodes",
      component:()=>import('../views/custom_nodes.vue')
    },
    {
      path:"/ComfyUI/installer",
      name:"ComfyUI installer",
      component:()=>import('../views/ComfyUI/ComfyUI_Installer.vue')
    }
  ],
})

export default router
