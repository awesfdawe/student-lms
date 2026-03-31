import { createRouter as _createRouter, createMemoryHistory, createWebHistory, type RouteRecordRaw } from 'vue-router'
import MainLayout from '../layout/MainLayout.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', name: 'landing', component: () => import('../views/LandingPage.vue') },
      { path: 'about', name: 'about', component: () => import('../views/AboutPage.vue') },
      { path: 'contacts', name: 'contacts', component: () => import('../views/ContactsPage.vue') },
      { path: 'courses', name: 'courses', component: () => import('../views/CoursePage.vue') },
      { path: 'faq', name: 'faq', component: () => import('../views/FaqPage.vue') },
      { path: 'free-courses', name: 'free-courses', component: () => import('../views/FreeCoursesPage.vue') },
      { path: 'login', name: 'login', component: () => import('../views/LoginPage.vue') },
      { path: 'register', name: 'register', component: () => import('../views/RegisterPage.vue') },
      { path: 'privacy-policy', name: 'privacy', component: () => import('../views/PrivacyPolicyPage.vue') },
      { path: 'terms-of-service', name: 'terms', component: () => import('../views/TermsOfServicePage.vue') },
      { path: ':pathMatch(.*)*', name: 'not-found', component: () => import('../views/NotFound.vue') }
    ]
  }
]

export function createRouter() {
  return _createRouter({
    history: import.meta.env.SSR 
          ? createMemoryHistory(import.meta.env.BASE_URL) 
          : createWebHistory(import.meta.env.BASE_URL),
    routes
  })
}
