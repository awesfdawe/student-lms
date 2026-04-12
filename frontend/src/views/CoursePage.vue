<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <template v-if="course">
        <h1 class="text-4xl md:text-5xl font-bold mb-6 text-black animate-fade-up" v-text="course.title"></h1>
        
        <div class="bg-gray-100 p-6 rounded-2xl mb-8 animate-fade-up flex flex-col gap-2" style="animation-delay: 0.1s">
          <p class="text-lg text-black/80 font-medium">
            <span class="text-black font-bold">{{ t('course_label_duration') }}</span> {{ course.duration }}
          </p>
          <p class="text-lg text-black/80 font-medium">
            <span class="text-black font-bold">{{ t('course_label_feature') }}</span> {{ course.feature }}
          </p>
        </div>

        <div class="prose max-w-[50rem] text-black/80 animate-fade-up" style="animation-delay: 0.2s" v-html="course.description || ''"></div>

        <div class="mt-10 flex gap-4 animate-fade-up" style="animation-delay: 0.3s">
          <router-link to="/register" class="btn-cta">{{ t('course_btn_enroll') }}</router-link>
          <button @click="router.back()" class="btn-cta !bg-gray-200 !text-black hover:!bg-gray-300">
            {{ t('global_btn_back') }}
          </button>
        </div>
      </template>

      <template v-else-if="isLoaded">
        <h1 class="text-4xl font-bold mb-6 text-black">{{ t('course_not_found_title') }}</h1>
        <p class="text-lg text-black/70">{{ t('course_not_found_desc') }}</p>
        <button @click="router.back()" class="btn-cta mt-6 !bg-gray-200 !text-black hover:!bg-gray-300">
          {{ t('global_btn_back') }}
        </button>
      </template>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { computed, onServerPrefetch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import { useContent } from '@/composables/useContent'

const route = useRoute()
const router = useRouter()
const { fetchCourse, fetchContent, isLoaded, t, store } = useContent()

const slug = computed(() => route.params.slug as string)
const course = computed(() => store.courses[slug.value])

const loadData = async () => {
  await fetchContent()
  if (slug.value) {
    await fetchCourse(slug.value)
  }
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!course.value || !isLoaded.value) {
    loadData()
  }
})
</script>
