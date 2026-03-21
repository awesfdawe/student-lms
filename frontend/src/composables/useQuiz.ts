import { ref, computed } from 'vue'
import { quizData } from '../data/quiz'

export function useQuiz() {
  const currentQuestionIndex = ref(0)
  const experienceScore = ref(0)
  const isFinished = ref(false)
  const totalQuestions = quizData.length

  const currentQuestion = computed(() => {
    return quizData[currentQuestionIndex.value] || null
  })

  const profession = computed(() => {
    if (experienceScore.value >= 25) return 'Программист'
    if (experienceScore.value >= 10) return 'UX/UI дизайнер'
    return '3D-дизайнер'
  })

  const courseLink = computed(() => {
    if (experienceScore.value >= 25) return '/course/programmer'
    if (experienceScore.value >= 10) return '/course/ux-ui'
    return '/course/3d-designer'
  })

  const resultText = computed(() => {
    if (experienceScore.value >= 25) {
      return 'Тебе подходит продвинутый трек. Мы подготовим сложную, ускоренную программу, фокусируясь на создании глубокого пет-проекта для твоего портфолио.'
    } else if (experienceScore.value >= 10) {
      return 'Тебе подходит базовый трек. Программа начнется с углубленного повторения основ и быстро перейдет к практическим задачам и командной работе.'
    } else {
      return "Тебе подходит трек 'С нуля'. Мы выстроим последовательную, пошаговую программу от самых азов, с упором на наставничество и помощь на каждом этапе."
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

  return {
    currentQuestionIndex,
    experienceScore,
    isFinished,
    totalQuestions,
    currentQuestion,
    resultText,
    profession,
    courseLink,
    handleAnswer,
    resetQuiz,
  }
}
