<template>
  <footer class="footer-wrapper">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="font-geologica font-bold text-[1.5rem] text-[#2D3149]">СКИЛЛФОРДЖ</div>
        <p class="text-[0.9375rem] text-black/60">{{ globals.footer_description }}</p>
      </div>
      
      <nav class="footer-nav">
        <router-link to="/free" class="footer-nav-link">{{ t('header_nav_free') }}</router-link>
        <router-link to="/about" class="footer-nav-link">{{ t('header_nav_about') }}</router-link>
        <router-link to="/contacts" class="footer-nav-link">{{ t('header_nav_contacts') }}</router-link>
        <router-link to="/faq" class="footer-nav-link">{{ t('header_nav_faq') }}</router-link>
      </nav>

      <div class="footer-cta-container">
        <div class="flex flex-col items-end gap-2">
          <a :href="'tel:' + globals.phone" class="font-bold text-[1.125rem] text-[#2D3149] hover:text-[var(--color-accent)] transition-colors">{{ globals.phone }}</a>
          <a :href="'mailto:' + globals.email" class="text-[0.9375rem] text-black/60 hover:text-[var(--color-accent)] transition-colors">{{ globals.email }}</a>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <div class="text-black/50">{{ globals.footer_copyright || '© 2026 ООО СКИЛЛФОРДЖ' }}</div>
      <div class="footer-bottom-links">
        <router-link to="/privacy-policy" class="footer-bottom-link">{{ t('footer_bottom_privacy', 'Политика конфиденциальности') }}</router-link>
        <router-link to="/terms-of-service" class="footer-bottom-link">{{ t('footer_bottom_terms', 'Пользовательское соглашение') }}</router-link>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { globals, t } = useContent()
</script>
