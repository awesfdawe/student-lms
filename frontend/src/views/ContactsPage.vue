<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <template v-if="pageData">
        <h1 class="text-4xl font-bold mb-6 text-black" v-text="pageData.title"></h1>
        <div class="prose max-w-none text-black/80" v-html="pageData.content || ''"></div>
        <div class="prose max-w-none mt-8 text-black/80" v-if="pageData.additional_content" v-html="pageData.additional_content"></div>
      </template>
      <template v-else>
        <div class="flex items-center justify-center h-full pt-[10rem]">
          <p class="text-xl text-black/50">{{ t('system_loading') }}</p>
        </div>
      </template>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { computed, onServerPrefetch, onMounted } from 'vue'
import MainLayout from '@/layout/MainLayout.vue'
import { useContent } from '@/composables/useContent'

const { fetchPage, fetchContent, store, t } = useContent()
const pageData = computed(() => store.pages['contacts'])

const loadData = async () => {
  await fetchContent()
  await fetchPage('contacts')
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!pageData.value) {
    loadData()
  }
})
</script>
