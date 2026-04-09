<template>
  <router-view />
  <CookieBanner />
</template>

<script setup lang="ts">
import { onServerPrefetch, onMounted } from 'vue'
import CookieBanner from '@/components/CookieBanner.vue'
import { useContent } from '@/composables/useContent'

const { fetchContent, isLoaded } = useContent()

const loadData = async () => {
  await fetchContent()
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!isLoaded.value) {
    loadData()
  }
})
</script>

<style>
@import '@/assets/style.css';
</style>
