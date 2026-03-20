<template>
  <MainLayout>
    <div class="hero-wrapper">
      <HeroSection />
    </div>
    <CoursesSection />
    <QuizSection />
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
import HeroSection from '@/components/hero/HeroSection.vue'
import CoursesSection from '@/components/courses/CoursesSection.vue'
import QuizSection from '@/components/quiz/QuizSection.vue'
</script>
