<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <div v-if="pageData" class="mb-8">
        <h1 class="text-4xl font-bold mb-6 text-black" v-text="pageData.title"></h1>
        <div class="prose max-w-none text-black/80" v-html="pageData.content || ''"></div>
        <div class="prose max-w-none mt-8 text-black/80" v-if="pageData.additional_content" v-html="pageData.additional_content"></div>
      </div>
      
      <div class="max-w-md mx-auto bg-white p-8 border border-gray-200 rounded-lg shadow-sm">
        <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Регистрация</h2>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div v-if="error" class="p-3 bg-red-100 text-red-700 rounded-md text-sm">
            {{ error }}
          </div>
          <div v-if="success" class="p-3 bg-green-100 text-green-700 rounded-md text-sm">
            Регистрация успешна! Перенаправление на страницу входа...
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
              minlength="8"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Подтвердите пароль</label>
            <input 
              v-model="form.passwordConfirm" 
              type="password" 
              required 
              minlength="8"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
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
