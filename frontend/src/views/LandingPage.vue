<template>
  <MainLayout>
    <div class="hero-wrapper">
      <HeroSection />
    </div>
    <CoursesSection />
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
import HeroSection from '@/components/hero/HeroSection.vue'
import CoursesSection from '@/components/courses/CoursesSection.vue'
</script>
