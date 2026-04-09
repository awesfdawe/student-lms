<template>
  <footer class="bg-gray-100 py-10 mt-auto border-t border-gray-200">
    <div class="layout-container grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="flex flex-col gap-4">
        <div class="font-bold text-2xl text-black">SKILLFORGE</div>
        <p class="text-black/70">{{ globals.footer_description }}</p>
        <p class="text-sm text-black/50">{{ globals.footer_license }}</p>
      </div>
      
      <div class="flex flex-col gap-3">
        <a :href="'tel:' + globals.phone" class="font-bold text-lg hover:text-primary transition-colors">{{ globals.phone }}</a>
        <a :href="'mailto:' + globals.email" class="hover:text-primary transition-colors">{{ globals.email }}</a>
        <p class="text-black/70">{{ globals.office_address }}</p>
      </div>

      <div class="flex flex-col gap-3">
        <router-link to="/privacy-policy" class="hover:text-primary transition-colors">{{ t('footer_bottom_privacy') }}</router-link>
        <router-link to="/terms-of-service" class="hover:text-primary transition-colors">{{ t('footer_bottom_terms') }}</router-link>
        <router-link to="/contacts" class="btn-cta text-center mt-2">{{ t('global_btn_contact_us') }}</router-link>
      </div>
    </div>
    <div class="layout-container mt-8 pt-6 border-t border-gray-200 text-center text-black/50">
      {{ globals.footer_copyright }}
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { globals, t } = useContent()
</script>
