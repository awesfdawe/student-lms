<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-10 xl:gap-[130px] mt-20 xl:mt-[100px] max-w-[960px] mx-auto animate-fade-up" style="animation-delay: 0.2s;">
    <HeroStatItem
      v-for="(stat, index) in stats"
      :key="index"
      :value="stat.value"
      :description="stat.description"
      :is-bold-value="stat.isBold"
    />
  </div>
</template>

<script setup>
import HeroStatItem from "./HeroStatItem.vue"

const stats = [
  { value: "100 000", description: "Студентов выбрали нас", isBold: true },
  { value: "90%", description: "Выпускников уже нашли себе работу", isBold: true },
  { value: "Первые", description: "В использовании ИИ в профессиональном обучении", isBold: false }
]
</script>