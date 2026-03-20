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
      <div
        class="w-full lg:w-[25rem] shrink-0 bg-gradient-to-b from-[rgba(229,186,186,0.6)] to-[rgba(224,131,131,0.86)] shadow-[8px_55px_160px_-27px_rgba(223,123,232,0.71)] rounded-[2rem] p-[1.5rem] md:p-[2rem] flex flex-col gap-[2rem]"
      >
        <transition name="fade-quiz" mode="out-in">
          <div
            v-if="!isFinished && currentQuestion"
            :key="currentQuestionIndex"
            class="flex flex-col gap-[2rem]"
          >
            <div
              class="bg-[#2D3149]/38 rounded-[3rem] p-[1.5rem] md:p-[2rem] relative min-h-[9.3125rem] flex items-center"
            >
              <h3
                class="font-geologica text-white text-[1.25rem] md:text-[1.5rem] leading-[1.4] md:leading-[1.875rem] pr-[1.5rem] md:pr-[2rem]"
              >
                {{ currentQuestion.title }}
              </h3>
              <span class="absolute bottom-[1.5rem] right-[2rem] text-white font-black text-[1rem]">
                {{ currentQuestionIndex + 1 }}/{{ totalQuestions }}
              </span>
            </div>

            <div class="flex flex-col gap-[1rem]">
              <button
                v-for="answer in currentQuestion.answers"
                :key="answer.id"
                @click="handleAnswer(answer.experienceScore)"
                class="w-full bg-white transition-all h-[4.5rem] md:h-[5.75rem] rounded-[4.8rem] font-roboto text-[1rem] md:text-[1.25rem] text-[#3F3F3F] px-4 shadow-sm cursor-pointer hover:shadow-[inset_0_0_1.5125rem_0.1875rem_rgba(249,169,169,0.2),0_10px_20px_rgba(249,169,169,0.2)] hover:-translate-y-1 active:scale-95"
              >
                {{ answer.text }}
              </button>
            </div>
          </div>

          <div v-else-if="isFinished" :key="'result'" class="flex flex-col gap-[2rem] p-2">
            <div
              class="bg-[#2D3149]/38 rounded-[3rem] p-[2rem] min-h-[9.3125rem] flex flex-col items-center justify-center gap-2 text-center"
            >
              <h3 class="font-geologica text-white text-[1.5rem] md:text-[1.75rem] font-bold">
                Ваш план готов!
              </h3>
              <p class="font-geologica text-white text-[1rem]">Основан на вашем опыте</p>
            </div>
            <div class="bg-white/70 backdrop-blur-sm rounded-[2rem] p-6 text-left shadow-inner">
              <p class="font-roboto text-[1.125rem] leading-[1.6] text-black">
                {{ resultText }}
              </p>
            </div>
            <div class="flex flex-col gap-[1rem] mt-2">
              <button class="btn-cta w-full">Получить полную программу</button>
              <button
                @click="resetQuiz"
                class="w-full h-[3.5rem] flex items-center justify-center font-geologica font-bold text-[0.9375rem] text-white/80 hover:text-white transition-colors cursor-pointer"
              >
                Пройти заново
              </button>
            </div>
          </div>
        </transition>
      </div>

      <div class="w-full lg:w-1/2 flex flex-col gap-[1.5rem] text-left lg:text-right">
        <h2 class="font-geologica font-bold text-[2.5rem] md:text-[3rem] leading-[1.2] text-black">
          Ответь на несколько вопросов
        </h2>
        <p
          class="font-roboto font-normal text-[1rem] md:text-[1.25rem] leading-[1.4] text-black tracking-[0.03em] lg:ml-auto max-w-[34.375rem]"
        >
          Это необходимо для проверки твоих знаний и подбора
          <span class="text-accent-dark">индивидуального</span> плана обучения
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const sectionRef = ref<HTMLElement | null>(null) // Ссылка объявлена как sectionRef
const isVisible = ref(false)
let observer: IntersectionObserver | null = null

const totalQuestions = 5
const currentQuestionIndex = ref(0)
const experienceScore = ref(0)
const isFinished = ref(false)

const quizData = [
  {
    title: 'Есть ли у тебя опыт с этой профессией?',
    answers: [
      { id: 1, text: 'Да, просто хочу подтянуть знания', experienceScore: 10 },
      { id: 2, text: 'Да, но совсем немного', experienceScore: 5 },
      { id: 3, text: 'Нет, буду учиться с нуля', experienceScore: 0 },
    ],
  },
  {
    title: 'Какую сферу обучения ты рассматриваешь?',
    answers: [
      { id: 4, text: 'Программирование и код', experienceScore: 0 },
      { id: 5, text: 'UX/UI и веб-дизайн', experienceScore: 0 },
      { id: 6, text: '3D-графика и моделирование', experienceScore: 0 },
    ],
  },
  {
    title: 'Как ты оцениваешь свою техническую грамотность?',
    answers: [
      { id: 7, text: 'Уверенно пишу код / работаю в редакторах', experienceScore: 10 },
      { id: 8, text: 'Разбираюсь в ПК на уровне продвинутого пользователя', experienceScore: 5 },
      { id: 9, text: 'Только начинаю осваивать', experienceScore: 0 },
    ],
  },
  {
    title: 'Какой темп обучения тебе подходит?',
    answers: [
      { id: 10, text: 'Интенсивный (3-4 часа в день)', experienceScore: 0 },
      { id: 11, text: 'Стандартный (1-2 часа в день)', experienceScore: 0 },
      { id: 12, text: 'Размеренный (выходные дни)', experienceScore: 0 },
    ],
  },
  {
    title: 'Какова твоя главная цель обучения?',
    answers: [
      { id: 13, text: 'Быстро найти первую работу', experienceScore: 5 },
      { id: 14, text: 'Сменить профессию / сферу', experienceScore: 5 },
      { id: 15, text: 'Реализовать свой пет-проект', experienceScore: 10 },
    ],
  },
]

const currentQuestion = computed(() => {
  return quizData[currentQuestionIndex.value] || null
})

const resultText = computed(() => {
  if (experienceScore.value >= 25) {
    return 'Вам подходит продвинутый трек. Мы подготовим сложную, ускоренную программу, фокусируясь на создании глубокого пет-проекта для вашего портфолио.'
  } else if (experienceScore.value >= 10) {
    return 'Вам подходит базовый трек. Программа начнется с углубленного повторения основ и быстро перейдет к практическим задачам и командной работе.'
  } else {
    return "Вам подходит трек 'С нуля'. Мы выстроим последовательную, пошаговую программу от самых азов, с упором на наставничество и помощь на каждом этапе."
  }
})

function handleAnswer(scoreToAdd: number) {
  experienceScore.value += scoreToAdd
  if (currentQuestionIndex.value < totalQuestions - 1) {
    currentQuestionIndex.value++
  } else {
    isFinished.value = true
  }
}

function resetQuiz() {
  currentQuestionIndex.value = 0
  experienceScore.value = 0
  isFinished.value = false
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      const entry = entries[0]
      if (entry?.isIntersecting) {
        isVisible.value = true
        // ИСПРАВЛЕНО: используем sectionRef вместо statsRef
        if (sectionRef.value) observer?.unobserve(sectionRef.value)
      }
    },
    { threshold: 0.1 },
  )

  if (sectionRef.value) {
    observer.observe(sectionRef.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
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
