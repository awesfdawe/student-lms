<template>
  <footer
    class="w-full py-[2.5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto flex flex-col lg:flex-row items-center justify-between gap-[2rem] lg:gap-8 border-t border-gray-100 mt-auto bg-white relative z-10"
  >
    <div class="flex flex-col items-center lg:items-start gap-2">
      <HeaderLogo />
      <span class="font-roboto text-[0.9375rem] text-black mt-2 lg:mt-0"
        >© 2026 ООО "СКИЛЛФОРДЖ"</span
      >
    </div>

    <nav
      class="flex flex-col md:flex-row items-center gap-[1.5rem] md:gap-[3.75rem] font-roboto text-[0.9375rem]"
    >
      <router-link to="/faq" class="text-black hover:text-accent transition-colors duration-200"
        >Частые вопросы</router-link
      >
      <router-link to="/free" class="text-black hover:text-accent transition-colors duration-200"
        >Бесплатные курсы</router-link
      >
      <router-link to="/about" class="text-black hover:text-accent transition-colors duration-200"
        >О нас</router-link
      >
      <router-link
        to="/contacts"
        class="text-black hover:text-accent transition-colors duration-200"
        >Контакты</router-link
      >
    </nav>

    <router-link to="/contacts" class="btn-cta shrink-0"> Свяжитесь с нами </router-link>
  </footer>
</template>

<script setup lang="ts">
import HeaderLogo from '../header/HeaderLogo.vue'
</script>
