<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <div v-if="pageData" class="mb-[4rem] text-center">
        <h1 class="text-h2 mb-[1.5rem]" v-text="pageData.title"></h1>
        <div class="text-body text-black/60 max-w-[40rem] mx-auto" v-html="pageData.content || ''"></div>
      </div>
      
      <div class="auth-card">
        <h2 class="text-[1.75rem] font-bold mb-[2.5rem] text-center text-[#2D3149]">
          {{ step === 1 ? 'Вход' : 'Двухфакторная авторизация' }}
        </h2>
        
        <form v-if="step === 1" @submit.prevent="handleLogin" class="space-y-[1.5rem]">
          <div v-if="error" class="p-[1rem] bg-red-50 text-red-600 rounded-[1rem] text-[0.9375rem] text-center font-medium">
            {{ error }}
          </div>
          
          <div>
            <label class="form-label">Email</label>
            <input 
              v-model="form.email" 
              type="email" 
              required 
              class="input-base"
            />
          </div>
          
          <div>
            <label class="form-label">Пароль</label>
            <input 
              v-model="form.password" 
              type="password" 
              required 
              class="input-base"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="btn-primary mt-[1rem]"
          >
            {{ loading ? 'Загрузка...' : 'Войти' }}
          </button>
        </form>

        <form v-else @submit.prevent="handle2fa" class="space-y-[1.5rem]">
          <div v-if="error" class="p-[1rem] bg-red-50 text-red-600 rounded-[1rem] text-[0.9375rem] text-center font-medium">
            {{ error }}
          </div>
          <p class="text-center text-[#3F3F3F] text-[0.9375rem] mb-[1rem]">
            Введите код из приложения-аутентификатора или резервный код восстановления.
          </p>
          
          <div>
            <label class="form-label text-center">Код</label>
            <input 
              v-model="twoFactorCode" 
              type="text" 
              required 
              class="input-base text-center tracking-[0.5em] text-[1.25rem] font-bold"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="btn-primary mt-[1rem]"
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
