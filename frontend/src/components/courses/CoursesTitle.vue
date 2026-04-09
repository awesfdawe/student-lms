<template>
  <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 animate-fade-up">
    <div class="max-w-[40rem]">
      <h2 class="text-3xl md:text-5xl font-bold text-black mb-4">
        {{ landingPage.courses_title || 'Наши курсы' }}
      </h2>
      <p class="text-lg text-black/70">
        {{ landingPage.courses_desc_1 || 'Развивайся вместе с нами' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { landingPage } = useContent()
</script>
