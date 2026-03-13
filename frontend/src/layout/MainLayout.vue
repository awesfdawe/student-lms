<template>
  <div class="flex flex-col min-h-screen">
    <Header />
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>

<script setup>
import Header from "../components/header/Header.vue"
</script>