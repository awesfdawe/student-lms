<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <div v-if="pageData" class="mb-8">
        <h1 class="text-4xl font-bold mb-6 text-black" v-text="pageData.title"></h1>
        <div class="prose max-w-none text-black/80" v-html="pageData.content || ''"></div>
      </div>
      
      <div class="max-w-md mx-auto bg-white p-8 border border-gray-200 rounded-lg shadow-sm">
        <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">
          {{ step === 1 ? 'Вход' : 'Двухфакторная авторизация' }}
        </h2>
        
        <form v-if="step === 1" @submit.prevent="handleLogin" class="space-y-4">
          <div v-if="error" class="p-3 bg-red-100 text-red-700 rounded-md text-sm">
            {{ error }}
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ loading ? 'Загрузка...' : 'Войти' }}
          </button>
        </form>

        <form v-else @submit.prevent="handle2fa" class="space-y-4">
          <div v-if="error" class="p-3 bg-red-100 text-red-700 rounded-md text-sm">
            {{ error }}
          </div>
          <p class="text-sm text-gray-600 mb-4">
            Введите код из приложения-аутентификатора или резервный код восстановления.
          </p>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Код</label>
            <input 
              v-model="twoFactorCode" 
              type="text" 
              required 
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 tracking-widest text-center text-lg"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ loading ? 'Проверка...' : 'Подтвердить' }}
          </button>
        </form>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onServerPrefetch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import { useContent } from '@/composables/useContent'
import { authApi, sanitizeEmail, sanitizePassword } from '@/api/auth'

const { fetchPage, fetchContent, store } = useContent()
const pageData = computed(() => store.pages['login'])
const router = useRouter()

const step = ref(1)
const form = ref({ email: '', password: '' })
const twoFactorCode = ref('')
const tempToken = ref('')
const error = ref('')
const loading = ref(false)

const loadData = async () => {
  await fetchContent()
  await fetchPage('login')
}

const handleLogin = async () => {
  error.value = ''
  const cleanEmail = sanitizeEmail(form.value.email)
  const cleanPassword = sanitizePassword(form.value.password)
  
  if (!cleanEmail || !cleanPassword) return
  
  loading.value = true
  try {
    const res = await authApi.login({ email: cleanEmail, password: cleanPassword })
    if (res.temp_token) {
      tempToken.value = res.temp_token
      step.value = 2
    } else if (res.access_token) {
      if (typeof window !== 'undefined') localStorage.setItem('access_token', res.access_token)
      router.push('/profile')
    }
  } catch (err: any) {
    error.value = err.detail || 'Неверный email или пароль.'
  } finally {
    loading.value = false
  }
}

const handle2fa = async () => {
  error.value = ''
  const cleanCode = twoFactorCode.value.replace(/[^a-zA-Z0-9]/g, '')
  if (!cleanCode) return
  
  loading.value = true
  try {
    const res = await authApi.verify2fa({ temp_token: tempToken.value, code: cleanCode })
    if (res.access_token) {
      if (typeof window !== 'undefined') localStorage.setItem('access_token', res.access_token)
      router.push('/profile')
    }
  } catch (err: any) {
    error.value = err.detail || 'Неверный код.'
  } finally {
    loading.value = false
  }
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!pageData.value) loadData()
})
</script>
