<template>
  <footer class="footer-wrapper">
    <div class="footer-top">
      <div class="footer-brand">
        <HeaderLogo />
        <span class="font-roboto text-[0.9375rem] text-black mt-2 font-bold">
          © 2026 ООО "СКИЛЛФОРДЖ"
        </span>
        <span class="font-roboto text-[0.875rem] text-black/50 text-center lg:text-left">
          Образовательная платформа для изучения востребованных digital-профессий
        </span>
      </div>

      <nav class="footer-nav">
        <router-link to="/faq" class="footer-nav-link">Частые вопросы</router-link>
        <router-link to="/free" class="footer-nav-link">Бесплатные курсы</router-link>
        <router-link to="/about" class="footer-nav-link">О нас</router-link>
        <router-link to="/contacts" class="footer-nav-link">Контакты</router-link>
      </nav>

      <div class="footer-cta-container">
        <div class="btn-wrap-smart">
          <router-link to="/contacts" class="btn-cta btn-mobile-right">Свяжись с нами</router-link>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="footer-bottom-links">
        <router-link to="/privacy" class="footer-bottom-link"
          >Политика конфиденциальности</router-link
        >
        <router-link to="/terms" class="footer-bottom-link">Публичная оферта</router-link>
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
