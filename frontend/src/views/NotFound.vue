<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[10rem] text-center min-h-[calc(100vh-5.625rem)]">
      <h1 class="text-6xl font-bold mb-4">{{ pageData?.title || store.t('404_title') }}</h1>
      <div class="prose max-w-none mx-auto mb-8" v-html="pageData?.content || 'Страница не найдена'"></div>
      <router-link to="/" class="btn-cta inline-block">{{ store.t('global_btn_home') }}</router-link>
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
