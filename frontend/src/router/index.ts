import { createRouter as _createRouter, createWebHistory, createMemoryHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import CoursePage from '@/views/CoursePage.vue'
import FreeCoursesPage from '@/views/FreeCoursesPage.vue'
import AboutPage from '@/views/AboutPage.vue'
import ContactsPage from '@/views/ContactsPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import FaqPage from '@/views/FaqPage.vue'
import PrivacyPolicyPage from '@/views/PrivacyPolicyPage.vue'
import TermsOfServicePage from '@/views/TermsOfServicePage.vue'
import NotFound from '@/views/NotFound.vue'

export function createRouter() {
  return _createRouter({
    history: import.meta.env.SSR ? createMemoryHistory() : createWebHistory(import.meta.env.BASE_URL),
    routes: [
      {
        path: '/',
        name: 'home',
        component: LandingPage,
      },
      {
        path: '/course/:slug',
        name: 'course',
        component: CoursePage,
      },
      {
        path: '/free',
        name: 'free-courses',
        component: FreeCoursesPage,
      },
      {
        path: '/about',
        name: 'about',
        component: AboutPage,
      },
      {
        path: '/contacts',
        name: 'contacts',
        component: ContactsPage,
      },
      {
        path: '/login',
        name: 'login',
        component: LoginPage,
      },
      {
        path: '/register',
        name: 'register',
        component: RegisterPage,
      },
      {
        path: '/faq',
        name: 'faq',
        component: FaqPage,
      },
      {
        path: '/privacy-policy',
        name: 'privacy-policy',
        component: PrivacyPolicyPage,
      },
      {
        path: '/terms-of-service',
        name: 'terms-of-service',
        component: TermsOfServicePage,
      },
      {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: NotFound,
      },
    ],
    scrollBehavior(to, from, savedPosition) {
      if (savedPosition) {
        return savedPosition
      } else {
        return { top: 0 }
      }
    },
  })
}
