import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'landing', component: () => import('@/views/LandingPage.vue') },
    { path: '/course/:id', name: 'course', component: () => import('@/views/CoursePage.vue') },
    { path: '/faq', name: 'faq', component: () => import('@/views/FaqPage.vue') },
    { path: '/free', name: 'free', component: () => import('@/views/FreeCoursesPage.vue') },
    { path: '/about', name: 'about', component: () => import('@/views/AboutPage.vue') },
    { path: '/contacts', name: 'contacts', component: () => import('@/views/ContactsPage.vue') },
    { path: '/login', name: 'login', component: () => import('@/views/LoginPage.vue') },
    { path: '/register', name: 'register', component: () => import('@/views/RegisterPage.vue') },
    { path: '/privacy', name: 'privacy', component: () => import('@/views/PrivacyPolicyPage.vue') },
    { path: '/terms', name: 'terms', component: () => import('@/views/TermsOfServicePage.vue') },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
    },
  ],
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0 }
  },
})

export default router
