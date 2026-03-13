<template>
  <div class="flex flex-col md:flex-row items-center justify-center gap-4 xl:gap-[49px] animate-fade-up">
    <a 
      href="#test" 
      class="btn-cta hero-start scale-75 md:scale-100 shrink-0 cursor-pointer"
    >
      {{ highlightText }}
    </a>
    <h1 class="font-geologica font-normal text-4xl md:text-[64px] md:leading-[80px] text-center md:text-left text-black">
      {{ mainText }}
    </h1>
  </div>
</template>

<script setup>
defineProps({
  highlightText: {
    type: String,
    default: "Начни"
  },
  mainText: {
    type: String,
    default: "свой путь с нами!" 
  }
})
</script>