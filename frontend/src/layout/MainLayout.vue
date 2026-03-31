<template>
  <div class="flex flex-col min-h-screen">
    <Header />
    <main class="flex-1">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/header/Header.vue'
import Footer from '@/components/footer/Footer.vue'
</script>
