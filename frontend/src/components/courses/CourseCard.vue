<template>
  <router-link
    :to="link"
    class="relative overflow-hidden rounded-[3.125rem] group cursor-pointer h-[20.9375rem] w-full flex flex-col justify-end shadow-md hover:shadow-xl transition-shadow duration-500 block"
  >
    <div
      class="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-110"
      :style="{ backgroundImage: bgImage }"
    ></div>

    <div
      class="relative w-full h-[6.0625rem] bg-[#2b2b2b]/[0.73] rounded-b-[3.125rem] flex flex-col justify-center px-[1.5rem] md:px-[2rem] z-10 transition-colors duration-300 group-hover:bg-[#2b2b2b]/90"
    >
      <h3
        class="font-roboto font-bold text-[1.5rem] md:text-[1.75rem] text-white tracking-[0.01em]"
      >
        {{ title }}
      </h3>
      <p class="font-roboto font-bold text-[0.875rem] md:text-[1rem] text-white/64 mt-[0.25rem]">
        {{ duration }} <span class="mx-[0.25rem]">|</span> {{ feature }}
      </p>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  duration: string
  feature: string
  image: string
  link?: string
}

const props = withDefaults(defineProps<Props>(), {
  link: '#',
})

const bgImage = computed(() => {
  const img = props.image
  if (!img) return 'none'
  if (img.startsWith('http') || img.startsWith('/api/')) {
    return `url('${img}')`
  }
  return `url('/api/v1/files/${img.split('/').pop()}')`
})
</script>
