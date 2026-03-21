<template>
  <div class="flex flex-col gap-[2rem]">
    <div class="quiz-question-box">
      <h3
        class="font-geologica text-white text-[1.25rem] md:text-[1.5rem] leading-[1.4] md:leading-[1.875rem] pr-[1.5rem] md:pr-[2rem]"
      >
        {{ question.title }}
      </h3>
      <span class="absolute bottom-[1.5rem] right-[2rem] text-white font-black text-[1rem]">
        {{ currentIndex + 1 }}/{{ total }}
      </span>
    </div>
    <div class="flex flex-col gap-[1rem]">
      <button
        v-for="answer in question.answers"
        :key="answer.id"
        @click="$emit('answer', answer.experienceScore)"
        class="quiz-btn"
      >
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  question: { title: string; answers: { id: number; text: string; experienceScore: number }[] }
  currentIndex: number
  total: number
}>()

defineEmits<{
  (e: 'answer', score: number): void
}>()
</script>
