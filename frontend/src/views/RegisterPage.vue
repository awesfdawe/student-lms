<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <div v-if="pageData" class="mb-[4rem] text-center">
        <h1 class="text-h2 mb-[1.5rem]" v-text="pageData.title"></h1>
        <div class="text-body text-black/60 max-w-[40rem] mx-auto" v-html="pageData.content || ''"></div>
        <div class="text-body text-black/60 max-w-[40rem] mx-auto mt-[1rem]" v-if="pageData.additional_content" v-html="pageData.additional_content"></div>
      </div>
      
      <div class="auth-card">
        <h2 class="text-[1.75rem] font-bold mb-[2.5rem] text-center text-[#2D3149]">Регистрация</h2>
        
        <form @submit.prevent="handleSubmit" class="space-y-[1.5rem]">
          <div v-if="error" class="p-[1rem] bg-red-50 text-red-600 rounded-[1rem] text-[0.9375rem] text-center font-medium">
            {{ error }}
          </div>
          <div v-if="success" class="p-[1rem] bg-green-50 text-green-600 rounded-[1rem] text-[0.9375rem] text-center font-medium">
            Регистрация успешна! Перенаправление на страницу входа...
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
              minlength="8"
              class="input-base"
            />
          </div>

          <div>
            <label class="form-label">Подтвердите пароль</label>
            <input 
              v-model="form.passwordConfirm" 
              type="password" 
              required 
              minlength="8"
              class="input-base"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="btn-primary mt-[1rem]"
          >
            {{ loading ? 'Загрузка...' : 'Зарегистрироваться' }}
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

const { fetchPage, fetchContent, store, t } = useContent()
const pageData = computed(() => store.pages['register'])
const router = useRouter()

const form = ref({ email: '', password: '', passwordConfirm: '' })
const error = ref('')
const success = ref(false)
const loading = ref(false)

const loadData = async () => {
  await fetchContent()
  await fetchPage('register')
}

const handleSubmit = async () => {
  error.value = ''
  
  const cleanEmail = sanitizeEmail(form.value.email)
  const cleanPassword = sanitizePassword(form.value.password)
  
  if (!cleanEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(cleanEmail)) {
    error.value = 'Некорректный email адрес.'
    return
  }
  if (cleanPassword !== sanitizePassword(form.value.passwordConfirm)) {
    error.value = 'Пароли не совпадают.'
    return
  }
  
  loading.value = true
  try {
    await authApi.register({ email: cleanEmail, password: cleanPassword })
    success.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (err: any) {
    error.value = err.detail || 'Произошла ошибка при регистрации.'
  } finally {
    loading.value = false
  }
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!pageData.value) {
    loadData()
  }
})
</script>
