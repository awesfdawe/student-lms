<template>
  <section
    class="relative z-10 flex flex-col justify-center md:block min-h-[calc(100vh-5.625rem)] md:min-h-0 py-[2rem] md:py-0 md:pt-[16.6875rem] pb-[3rem] md:pb-[6rem] layout-container mt-[5.625rem] md:mt-0"
  >
    <div class="w-full">
      <HeroTitle />
      <HeroStats />
    </div>
  </section>
</template>

<script setup lang="ts">
import HeroTitle from './HeroTitle.vue'
import HeroStats from './HeroStats.vue'
</script>
