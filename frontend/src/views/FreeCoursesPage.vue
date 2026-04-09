<template>
  <MainLayout>
    <section class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto min-h-[calc(100vh-5.625rem)]">
      <template v-if="pageData">
        <h1 class="font-geologica font-bold text-[2.5rem] md:text-[4rem] text-black mb-[1rem] animate-fade-up" v-text="pageData.title"></h1>
        <div class="font-roboto text-[1.125rem] text-black/70 mb-[3rem] animate-fade-up max-w-[40rem] prose" style="animation-delay: 0.1s" v-html="pageData.content"></div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-[1.5rem] md:gap-[2.5rem] animate-fade-up mb-[3rem]" style="animation-delay: 0.2s">
          <CourseCard title="Основы дизайна" duration="1 неделя" feature="вводный курс" image="/src/assets/images/course-ux-ui.jpg" link="/course/ux-ui" />
          <CourseCard title="Введение в код" duration="2 недели" feature="вводный курс" image="/src/assets/images/course-programmer.jpg" link="/course/programmer" />
        </div>
        
        <div class="flex flex-wrap items-center gap-[1rem] w-full max-w-[30rem] animate-fade-up" style="animation-delay: 0.3s">
          <button @click="router.back()" class="btn-cta !bg-gray-200 !text-black hover:!bg-gray-300 flex-grow whitespace-nowrap text-center">{{ t('global_btn_back') }}</button>
          <router-link to="/" class="btn-cta flex-grow-[2] whitespace-nowrap text-center">{{ t('global_btn_home') }}</router-link>
        </div>
      </template>
      <template v-else>
        <div class="flex items-center justify-center h-full pt-[4rem]">
          <p class="text-xl text-black/50">{{ t('system_loading') }}</p>
        </div>
      </template>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import { computed, onServerPrefetch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import CourseCard from '@/components/courses/CourseCard.vue'
import { useContent } from '@/composables/useContent'

const router = useRouter()
const { fetchPage, fetchContent, store, t } = useContent()
const pageData = computed(() => store.pages['free_courses'])

const loadData = async () => {
  await fetchContent()
  await fetchPage('free_courses')
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!pageData.value) {
    loadData()
  }
})
</script>
