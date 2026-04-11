<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[10rem] text-center min-h-[calc(100vh-5.625rem)] flex flex-col items-center justify-center">
      <h1 class="text-[4rem] md:text-[6rem] font-geologica font-bold mb-[1.5rem] text-[#2D3149]">{{ pageData?.title || store.t('404_title', '404') }}</h1>
      <div class="text-body text-black/60 max-w-[40rem] mx-auto mb-[2.5rem]" v-html="pageData?.content || 'Страница не найдена'"></div>
      <router-link to="/" class="btn-primary max-w-[15rem]">{{ store.t('global_btn_home', 'На главную') }}</router-link>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { computed, onServerPrefetch, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import { useContent } from '@/composables/useContent'

const { fetchContent, fetchPage, store } = useContent()
const pageData = computed(() => store.pages['not_found'])

const loadData = async () => {
  await Promise.all([fetchContent(), fetchPage('not_found')])
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!pageData.value) loadData()
})
</script>
