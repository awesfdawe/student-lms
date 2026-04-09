<template>
  <nav class="hidden md:flex gap-6 items-center">
    <router-link to="/free" class="hover:text-primary transition-colors font-medium">{{ t('header_nav_free') }}</router-link>
    <router-link to="/about" class="hover:text-primary transition-colors font-medium">{{ t('header_nav_about') }}</router-link>
    <router-link to="/contacts" class="hover:text-primary transition-colors font-medium">{{ t('header_nav_contacts') }}</router-link>
    <router-link to="/faq" class="hover:text-primary transition-colors font-medium">{{ t('header_nav_faq') }}</router-link>
  </nav>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { t } = useContent()
</script>
