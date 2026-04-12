<template>
  <div 
    class="flex flex-col items-start gap-[2rem] max-w-[40rem] transition-all duration-1000 transform"
    :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[3rem]'"
  >
    <h1 class="text-[3rem] md:text-[4rem] leading-[1.1] font-bold text-black">
      <span class="text-[var(--color-accent)]">{{ landingPage.hero_highlight || 'Начни' }}</span> {{ landingPage.hero_main_text || 'свой путь с нами!' }}
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
import { ref, onMounted } from 'vue'
import { useContent } from '@/composables/useContent'

const { landingPage, t } = useContent()
const isVisible = ref(false)

onMounted(() => {
  setTimeout(() => {
    isVisible.value = true
  }, 50)
})

const scrollToQuiz = () => {
  const el = document.getElementById('quiz') || document.querySelector('.quiz-section') || document.querySelectorAll('section')[2]
  if (el) {
    const isMobile = window.innerWidth < 768
    const offsetFactor = isMobile ? 0.01 : 0.10
    
    const y = el.getBoundingClientRect().top + window.scrollY + (window.innerHeight * offsetFactor)
    
    window.scrollTo({ top: y, behavior: 'smooth' })
  } else {
    window.location.href = '/#quiz'
  }
}
</script>
