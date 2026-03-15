<template>
  <div
    class="flex flex-col md:flex-row items-start md:items-center justify-start md:justify-center gap-[0.25rem] md:gap-[3.0625rem] animate-fade-up w-full"
  >
    <div class="flex items-center gap-[0.5rem] md:gap-[3.0625rem] w-full md:w-auto">
      <router-link
        to="#test"
        class="btn-cta hero-start shrink-0 cursor-pointer !flex !items-center !justify-center !w-[11.5rem] !h-[4.5rem] !text-[2.5rem] !leading-none md:!w-[16.5625rem] md:!h-[6.5rem] md:!text-[4rem]"
      >
        {{ highlightText }}
      </router-link>

      <span class="md:hidden font-geologica font-normal text-[2.5rem] leading-[2.5rem] text-black">
        {{ firstWord }}
      </span>
    </div>

    <h1
      class="font-geologica font-normal text-[2.5rem] leading-[2.5rem] md:text-[4rem] md:leading-[5rem] text-left md:text-center text-black w-full md:w-auto"
    >
      <span class="hidden md:inline">{{ mainText }}</span>
      <span class="inline md:hidden">{{ restOfText }}</span>
    </h1>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  highlightText?: string
  mainText?: string
}

const props = withDefaults(defineProps<Props>(), {
  highlightText: 'Начни',
  mainText: 'свой путь с нами!',
})

const firstWord = computed(() => props.mainText.split(' ')[0] || '')
const restOfText = computed(() => {
  const words = props.mainText.split(' ')
  return words.slice(1).join(' ')
})
</script>
