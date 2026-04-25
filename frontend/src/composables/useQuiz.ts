import { ref, computed } from 'vue'
import { api } from '@/api/index'

export interface QuizAnswer {
  text: string
  experience_score: number
}

export interface QuizQuestion {
  id: number
  title: string
  answers: QuizAnswer[]
}

export function useQuiz() {
  const questions = ref<QuizQuestion[]>([])
  const currentQuestionIndex = ref(0)
  const experienceScore = ref(0)
  const isFinished = ref(false)
  const isLoading = ref(true)
  const error = ref<string | null>(null)

  const totalQuestions = computed(() => questions.value.length)

  const currentQuestion = computed(() => {
    return questions.value[currentQuestionIndex.value] || null
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
    if (currentQuestionIndex.value < totalQuestions.value - 1) {
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

  async function fetchQuizData() {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.get<QuizQuestion[]>('/cms/quiz')
      questions.value = response.data
    } catch (e: any) {
      error.value = 'Ошибка при загрузке вопросов.'
    } finally {
      isLoading.value = false
    }
  }

  return {
    questions,
    currentQuestionIndex,
    experienceScore,
    isFinished,
    isLoading,
    error,
    totalQuestions,
    currentQuestion,
    resultText,
    profession,
    courseLink,
    handleAnswer,
    resetQuiz,
    fetchQuizData
  }
}
