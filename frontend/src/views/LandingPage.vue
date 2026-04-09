<template>
  <MainLayout>
    <template v-if="isLoaded">
      <div class="hero-wrapper">
        <HeroSection />
      </div>
      <CoursesSection />
      <QuizSection />
    </template>
    <template v-else>
      <div class="flex items-center justify-center min-h-[calc(100vh-5.625rem)]">
        <p class="text-xl text-black/50">{{ t('system_loading') }}</p>
      </div>
    </template>
  </MainLayout>
</template>

<script setup lang="ts">
import { onServerPrefetch, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import HeroSection from '@/components/hero/HeroSection.vue'
import CoursesSection from '@/components/courses/CoursesSection.vue'
import QuizSection from '@/components/quiz/QuizSection.vue'
import { useContent } from '@/composables/useContent'

const { fetchContent, fetchCourses, isLoaded, t } = useContent()

const loadData = async () => {
  await Promise.all([
    fetchContent(),
    fetchCourses()
  ])
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!isLoaded.value) {
    loadData()
  }
})
</script>
