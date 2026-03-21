<template>
  <footer
    class="w-full pt-[3rem] pb-[2rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto flex flex-col border-t border-gray-100 mt-auto bg-white relative z-10"
  >
    <div
      class="flex flex-col lg:flex-row items-center justify-between gap-[2.5rem] mb-[2.5rem] w-full"
    >
      <div class="flex flex-col items-center lg:items-start gap-2 shrink-0">
        <HeaderLogo />
        <span class="font-roboto text-[0.9375rem] text-black mt-2 font-bold">
          © 2026 ООО "СКИЛЛФОРДЖ"
        </span>
        <span
          class="font-roboto text-[0.875rem] text-black/50 text-center lg:text-left max-w-[20rem]"
        >
          Образовательная платформа для изучения востребованных digital-профессий
        </span>
      </div>

      <nav
        class="flex flex-col lg:flex-row items-center justify-center flex-1 w-full gap-[1.5rem] lg:gap-[2.5rem] xl:gap-[3.75rem] font-roboto text-[0.9375rem] px-[2rem]"
      >
        <router-link
          to="/faq"
          class="text-black hover:text-accent transition-colors duration-200 whitespace-nowrap"
          >Частые вопросы</router-link
        >
        <router-link
          to="/free"
          class="text-black hover:text-accent transition-colors duration-200 whitespace-nowrap"
          >Бесплатные курсы</router-link
        >
        <router-link
          to="/about"
          class="text-black hover:text-accent transition-colors duration-200 whitespace-nowrap"
          >О нас</router-link
        >
        <router-link
          to="/contacts"
          class="text-black hover:text-accent transition-colors duration-200 whitespace-nowrap"
          >Контакты</router-link
        >
      </nav>

      <router-link to="/contacts" class="btn-cta shrink-0"> Свяжись с нами </router-link>
    </div>

    <div
      class="flex flex-col md:flex-row items-center justify-between gap-[1rem] pt-[1.5rem] border-t border-gray-100 font-roboto text-[0.75rem] text-black/40"
    >
      <div class="flex flex-wrap justify-center gap-[1rem] md:gap-[2rem]">
        <router-link to="/privacy" class="hover:text-accent transition-colors"
          >Политика конфиденциальности</router-link
        >
        <router-link to="/terms" class="hover:text-accent transition-colors"
          >Публичная оферта</router-link
        >
      </div>
      <div class="text-center md:text-right">
        Лицензия на осуществление образовательной деятельности № Л035-01298-77/00181484 от
        15.03.2026 г.
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import HeaderLogo from '../header/HeaderLogo.vue'
</script>
