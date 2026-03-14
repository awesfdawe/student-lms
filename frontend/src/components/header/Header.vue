<template>
  <header
    class="fixed top-0 left-0 w-full z-50 transition-all duration-300 backdrop-blur-md bg-white/70"
  >
    <div
      class="max-w-[80rem] mx-auto px-5 xl:px-[5.625rem] py-[1.25rem] xl:py-[2.125rem] flex items-center justify-between"
    >
      <HeaderLogo />

      <HeaderNav class="hidden lg:flex" />

      <div class="hidden lg:block">
        <HeaderCTA />
      </div>

      <button
        :aria-expanded="isMobileMenuOpen"
        aria-controls="mobile-menu"
        class="lg:hidden relative z-[70] p-2 text-black hover:opacity-70 transition-all flex items-center justify-center"
        aria-label="Toggle menu"
        @click="toggleMobileMenu"
      >
        <svg
          class="w-8 h-8 transition-transform duration-300"
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
      enter-from-class="opacity-0 -translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-4"
    >
      <div
        v-if="isMobileMenuOpen"
        id="mobile-menu"
        class="absolute top-0 left-0 w-full min-h-screen bg-white shadow-2xl flex flex-col items-center pt-[7.5rem] gap-10 lg:hidden z-[60]"
      >
        <HeaderNav is-mobile @click="closeMobileMenu" />
        <HeaderCTA />
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import HeaderLogo from './HeaderLogo.vue'
import HeaderNav from './HeaderNav.vue'
import HeaderCTA from './HeaderCTA.vue'

const isMobileMenuOpen = ref(false)

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

watch(isMobileMenuOpen, (isOpen) => {
  document.body.style.overflow = isOpen ? 'hidden' : ''
})
</script>