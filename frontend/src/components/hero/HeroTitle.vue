<template>
  <div class="flex flex-col items-start gap-[2rem] max-w-[40rem] animate-fade-up">
    <h1 class="text-[3rem] md:text-[4rem] leading-[1.1] font-bold text-black">
      <span class="text-[var(--color-accent)]">{{ landingPage.hero_highlight || landingPage.hero_title }}</span> {{ landingPage.hero_main_text || '' }}
    </h1>
    <p v-if="landingPage.hero_subtitle" class="text-body text-black/60">{{ landingPage.hero_subtitle }}</p>
    
    <div class="flex flex-col sm:flex-row items-start sm:items-center gap-[1.5rem] sm:gap-[2.5rem] mt-[1rem]">
      <a href="#quiz" @click.prevent="scrollToQuiz" class="btn-primary px-[2.5rem]">
        Подобрать профессию
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
const { landingPage, t } = useContent()

const scrollToQuiz = () => {
  const el = document.getElementById('quiz') || document.querySelector('.quiz-section') || document.querySelectorAll('section')[2]
  if (el) {
    const isMobile = window.innerWidth < 768
    const offsetFactor = isMobile ? 0.01 : 0.10
    console.log(isMobile)
    
    const y = el.getBoundingClientRect().top + window.scrollY + (window.innerHeight * offsetFactor)
    
    window.scrollTo({ 
      top: y, 
      behavior: 'smooth' 
    })
  } else {
    window.location.href = '/#quiz'
  }
}
</script>
