<template>
  <div
    class="grid grid-cols-1 md:grid-cols-3 gap-10 xl:gap-[8.125rem] mt-20 xl:mt-[6.25rem] max-w-[60rem] mx-auto animate-fade-up"
    style="animation-delay: 0.2s"
  >
    <HeroStatItem
      v-for="(stat, index) in stats"
      :key="index"
      :value="stat.value"
      :description="stat.description"
      :is-bold-value="stat.isBold"
    />
  </div>
</template>

<script setup lang="ts">
import HeroStatItem from './HeroStatItem.vue'

interface StatItem {
  value: string
  description: string
  isBold: boolean
}

const stats: StatItem[] = [
  { value: '100 000', description: 'Студентов выбрали нас', isBold: true },
  { value: '90%', description: 'Выпускников уже нашли себе работу', isBold: true },
  { value: 'Первые', description: 'В использовании ИИ в профессиональном обучении', isBold: false },
]
</script>
