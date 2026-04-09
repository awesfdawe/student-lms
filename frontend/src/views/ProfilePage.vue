<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <h1 class="text-4xl font-bold mb-8 text-black">Личный кабинет</h1>
      
      <div class="max-w-2xl bg-white p-8 border border-gray-200 rounded-lg shadow-sm">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Настройки безопасности</h2>
        
        <div v-if="error" class="p-3 mb-4 bg-red-100 text-red-700 rounded-md text-sm">
          {{ error }}
        </div>
        <div v-if="success" class="p-3 mb-4 bg-green-100 text-green-700 rounded-md text-sm">
          {{ success }}
        </div>

        <div v-if="!setupData">
          <p class="text-gray-600 mb-4">Обеспечьте дополнительную защиту вашего аккаунта, включив двухфакторную аутентификацию.</p>
          <button @click="init2fa" class="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 transition">
            Включить 2FA
          </button>
        </div>

        <div v-else class="space-y-6">
          <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h3 class="text-lg font-semibold mb-2">1. Отсканируйте QR-код</h3>
            <p class="text-sm text-gray-600 mb-4">Используйте Google Authenticator или Authy.</p>
            <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(setupData.otpauth_uri)}`" alt="QR Code" class="mx-auto mb-4 border p-2 bg-white" />
          </div>

          <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h3 class="text-lg font-semibold mb-2">2. Сохраните коды восстановления</h3>
            <p class="text-sm text-gray-600 mb-4">Если вы потеряете доступ к приложению, вы сможете использовать эти коды для входа.</p>
            <div class="grid grid-cols-2 gap-2 font-mono text-sm bg-white p-4 border rounded">
              <div v-for="(code, idx) in setupData.recovery_codes" :key="idx">{{ code }}</div>
            </div>
          </div>

          <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <h3 class="text-lg font-semibold mb-2">3. Подтвердите активацию</h3>
            <div class="flex gap-4">
              <input 
                v-model="confirmCode" 
                type="text" 
                placeholder="Код из приложения" 
                class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 tracking-widest"
              />
              <button @click="confirm2fa" class="bg-green-600 text-white py-2 px-6 rounded-md hover:bg-green-700 transition">
                Активировать
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'
import { authApi } from '@/api/auth'

const router = useRouter()
const error = ref('')
const success = ref('')
const setupData = ref<any>(null)
const confirmCode = ref('')

onMounted(() => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
    }
  }
})

const init2fa = async () => {
  error.value = ''
  try {
    const res = await authApi.enable2fa()
    setupData.value = res
  } catch (err: any) {
    error.value = err.detail || 'Ошибка при генерации 2FA.'
  }
}

const confirm2fa = async () => {
  error.value = ''
  const cleanCode = confirmCode.value.replace(/[^a-zA-Z0-9]/g, '')
  if (!cleanCode) return
  
  try {
    await authApi.confirm2fa(cleanCode)
    success.value = 'Двухфакторная аутентификация успешно включена!'
    setupData.value = null
  } catch (err: any) {
    error.value = err.detail || 'Неверный код подтверждения.'
  }
}
</script>
