<template>
  <div
    ref="statsRef"
    class="grid grid-cols-2 md:grid-cols-3 gap-[1rem] md:gap-[2.5rem] xl:gap-[8.125rem] mt-[3rem] xl:mt-[6.25rem] max-w-[60rem] mx-auto transition-all duration-1000 transform"
    :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[3rem]'"
  >
    <HeroStatItem
      v-for="(stat, index) in stats"
      :key="index"
      :value="stat.value"
      :description="stat.description"
      :is-bold-value="stat.isBold"
      :class="{ 'col-span-2 md:col-span-1': index === 2 }"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import HeroStatItem from './HeroStatItem.vue'

interface StatItem {
  value: string
  description: string
  isBold: boolean
}

const stats: StatItem[] = [
  { value: '100 000', description: 'Студентов выбрали нас', isBold: true },
  { value: '90%', description: 'Уже нашли работу', isBold: true },
  { value: 'Первые', description: 'В использовании ИИ в обучении', isBold: false },
]

const statsRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)
let observer: IntersectionObserver | null = null

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      const entry = entries[0]
      if (entry?.isIntersecting) {
        isVisible.value = true
        if (statsRef.value) observer?.unobserve(statsRef.value)
      }
    },
    { threshold: 0.1 },
  )

  if (statsRef.value) {
    observer.observe(statsRef.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>
