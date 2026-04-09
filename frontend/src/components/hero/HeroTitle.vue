<template>
  <div class="flex flex-col items-start gap-6 max-w-[40rem] animate-fade-up">
    <h1 class="text-[3rem] md:text-[4rem] leading-[1.1] font-bold text-black">
      <span class="text-primary">{{ landingPage.hero_highlight }}</span> {{ landingPage.hero_main_text }}
    </h1>
    <button @click="router.push('/free')" class="btn-cta text-lg py-3 px-8">{{ t('hero_cta_text') }}</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useContent } from '@/composables/useContent'

const router = useRouter()
const { landingPage, t } = useContent()
</script>
