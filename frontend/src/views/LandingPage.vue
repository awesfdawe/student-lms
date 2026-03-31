<template>
  <div class="hero-wrapper">
    <HeroSection />
  </div>
  <CoursesSection />
  <QuizSection />
</template>

<script setup lang="ts">
import HeroSection from '@/components/hero/HeroSection.vue'
import CoursesSection from '@/components/courses/CoursesSection.vue'
import QuizSection from '@/components/quiz/QuizSection.vue'
</script>
