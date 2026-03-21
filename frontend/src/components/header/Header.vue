<template>
  <header class="header-wrapper">
    <div
      class="header-content"
      :class="isScrolled ? 'py-[0.75rem] xl:py-[1rem]' : 'py-[1.25rem] xl:py-[2.125rem]'"
    >
      <HeaderLogo />

      <HeaderNav class="hidden lg:flex" />

      <div class="hidden lg:block">
        <HeaderCTA />
      </div>

      <button
        :aria-expanded="isMobileMenuOpen"
        aria-controls="mobile-menu"
        class="lg:hidden p-[0.5rem] text-black hover:opacity-70 transition-all flex items-center justify-center"
        aria-label="Toggle menu"
        @click="toggleMobileMenu"
      >
        <svg
          class="w-[2rem] h-[2rem] transition-transform duration-300"
          :class="{ 'rotate-45': isMobileMenuOpen }"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path v-if="!isMobileMenuOpen" d="M3 12h18M3 6h18M3 18h18" />
          <path v-else d="M18 6L6 18M6 6l12 12" />
        </svg>
      </button>
    </div>

    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 -translate-y-full"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-full"
    >
      <div
        v-if="isMobileMenuOpen"
        id="mobile-menu"
        class="absolute top-0 left-0 w-full min-h-screen bg-white/95 backdrop-blur-xl flex flex-col items-start pt-[7.5rem] z-40"
      >
        <HeaderNav is-mobile @close="closeMobileMenu" />

        <div class="w-full px-[2rem] mt-[3rem] mb-[4rem]">
          <div class="w-full h-[1px] bg-gray-200 mb-[2rem]"></div>
          <HeaderCTA full-width @click="closeMobileMenu" />
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import HeaderLogo from './HeaderLogo.vue'
import HeaderNav from './HeaderNav.vue'
import HeaderCTA from './HeaderCTA.vue'

const isMobileMenuOpen = ref(false)
const isScrolled = ref(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

function handleScroll() {
  isScrolled.value = window.scrollY > 50
}

watch(isMobileMenuOpen, (isOpen) => {
  document.body.style.overflow = isOpen ? 'hidden' : ''
})

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.body.style.overflow = ''
})
</script>
