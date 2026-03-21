<template>
  <section
    id="test"
    class="relative z-10 pt-[5rem] md:pt-[10rem] pb-[5rem] md:pb-[10rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto overflow-hidden"
  >
    <div
      ref="sectionRef"
      class="flex flex-col-reverse lg:flex-row items-center justify-between gap-[3rem] lg:gap-[5rem] transition-all duration-1000 transform"
      :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[3rem]'"
    >
      <div class="quiz-container w-full lg:w-1/2">
        <transition name="fade-quiz" mode="out-in">
          <QuizQuestionCard
            v-if="!isFinished && currentQuestion"
            :key="currentQuestionIndex"
            :question="currentQuestion"
            :current-index="currentQuestionIndex"
            :total="totalQuestions"
            @answer="handleAnswer"
          />
          <QuizResultCard
            v-else-if="isFinished"
            :key="'result'"
            :result-text="resultText"
            :course-link="courseLink"
            @reset="resetQuiz"
          />
        </transition>
      </div>

      <div class="w-full lg:w-1/2 flex flex-col gap-[1.5rem] text-left lg:text-right">
        <template v-if="!isFinished">
          <h2 class="text-h2">Ответь на несколько вопросов</h2>
          <p class="text-body lg:ml-auto max-w-[34.375rem]">
            Это необходимо для проверки твоих знаний и подбора
            <span class="text-accent-dark">индивидуального</span> плана обучения
          </p>
        </template>
        <template v-else>
          <h2 class="text-h2">Твой результат готов!</h2>
          <p class="text-body lg:ml-auto max-w-[34.375rem]">
            Ты прирожденный <span class="font-bold">{{ profession }}</span
            >! У нас есть для тебя специальный
            <router-link
              :to="courseLink"
              class="text-accent font-bold hover:text-accent-dark transition-colors"
              >курс</router-link
            >.
          </p>
        </template>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useIntersectionAnimation } from '../../composables/useIntersectionAnimation'
import { useQuiz } from '../../composables/useQuiz'
import QuizQuestionCard from './QuizQuestionCard.vue'
import QuizResultCard from './QuizResultCard.vue'

const sectionRef = ref<HTMLElement | null>(null)
const { isVisible } = useIntersectionAnimation(sectionRef)

const {
  currentQuestionIndex,
  isFinished,
  totalQuestions,
  currentQuestion,
  resultText,
  profession,
  courseLink,
  handleAnswer,
  resetQuiz,
} = useQuiz()
</script>

<style scoped>
.fade-quiz-enter-active,
.fade-quiz-leave-active {
  transition:
    opacity 0.4s ease,
    transform 0.4s ease;
}
.fade-quiz-enter-from {
  opacity: 0;
  transform: translateX(1.25rem);
}
.fade-quiz-leave-to {
  opacity: 0;
  transform: translateX(-1.25rem);
}
</style>
