<template>
  <div
    class="flex flex-col md:flex-row items-center justify-center gap-4 xl:gap-[3.0625rem] animate-fade-up"
  >
    <router-link
      to="#test"
      class="btn-cta hero-start scale-75 md:scale-100 shrink-0 cursor-pointer"
    >
      {{ highlightText }}
    </router-link>
    <h1
      class="font-geologica font-normal text-4xl md:text-[4rem] md:leading-[5rem] text-center md:text-left text-black"
    >
      {{ mainText }}
    </h1>
  </div>
</template>

<script setup lang="ts">
interface Props {
  highlightText?: string
  mainText?: string
}

withDefaults(defineProps<Props>(), {
  highlightText: 'Начни',
  mainText: 'свой путь с нами!',
})
</script>
