<template>
  <div class="flex flex-col items-start gap-[2rem] max-w-[40rem] animate-fade-up">
    <h1 class="text-[3rem] md:text-[4rem] leading-[1.1] font-bold text-black">
      <span class="text-[var(--color-accent)]">{{ landingPage.hero_highlight || landingPage.hero_title }}</span> {{ landingPage.hero_main_text || '' }}
    </h1>
    <p v-if="landingPage.hero_subtitle" class="text-body text-black/60">{{ landingPage.hero_subtitle }}</p>
    
    <div class="flex flex-col sm:flex-row items-start sm:items-center gap-[1.5rem] sm:gap-[2.5rem] mt-[1rem]">
      <router-link to="/free" class="btn-primary px-[2.5rem]">{{ t('hero_cta_text', 'Смотреть курсы') }}</router-link>
      <router-link to="/quiz" class="font-bold text-[#2D3149] hover:text-[var(--color-accent)] transition-colors flex items-center gap-2 group">
        Подобрать профессию 
        <i class="fa-solid fa-arrow-right text-[0.875rem] transform group-hover:translate-x-1 transition-transform"></i>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { landingPage, t } = useContent()
</script>
