<template>
  <div class="flex gap-4 items-center">
    <router-link to="/login" class="text-black hover:text-primary transition-colors font-medium">{{ t('header_cta_login') }}</router-link>
    <router-link to="/register" class="btn-cta py-2 px-5 text-sm">{{ t('header_cta_register') }}</router-link>
  </div>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { t } = useContent()
</script>
