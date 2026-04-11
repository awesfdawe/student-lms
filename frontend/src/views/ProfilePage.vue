<template>
  <MainLayout>
    <div class="page-wrapper layout-container py-[4rem] mt-[5.625rem] min-h-[calc(100vh-5.625rem)]">
      <h1 class="text-h2 mb-[2.5rem] text-center md:text-left text-[#2D3149]">Мой кабинет</h1>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-[2rem]">
        
        <div class="bg-white p-[2rem] md:p-[2.5rem] rounded-[2.5rem] shadow-[0_10px_40px_-10px_rgba(0,0,0,0.05)] border border-gray-50 flex flex-col gap-[1.5rem]">
          <h2 class="text-[1.5rem] font-bold text-[#2D3149]">Смена пароля</h2>
          
          <div v-if="pwdError" class="p-[1rem] bg-red-50 text-red-600 rounded-[1rem] text-[0.9375rem] font-medium">{{ pwdError }}</div>
          <div v-if="pwdSuccess" class="p-[1rem] bg-green-50 text-green-600 rounded-[1rem] text-[0.9375rem] font-medium">{{ pwdSuccess }}</div>
          
          <form @submit.prevent="changePassword" class="space-y-[1.25rem]">
            <div>
              <label class="form-label">Текущий пароль</label>
              <input v-model="pwdForm.old_password" type="password" required class="input-base" />
            </div>
            <div>
              <label class="form-label">Новый пароль</label>
              <input v-model="pwdForm.new_password" type="password" required minlength="8" class="input-base" />
            </div>
            <div>
              <label class="form-label">Подтвердите новый пароль</label>
              <input v-model="pwdForm.confirm_password" type="password" required minlength="8" class="input-base" />
            </div>
            <button type="submit" :disabled="pwdLoading" class="btn-primary mt-[1rem]">
              {{ pwdLoading ? 'Сохранение...' : 'Обновить пароль' }}
            </button>
          </form>
        </div>

        <div class="bg-white p-[2rem] md:p-[2.5rem] rounded-[2.5rem] shadow-[0_10px_40px_-10px_rgba(0,0,0,0.05)] border border-gray-50 flex flex-col gap-[1.5rem]">
          <h2 class="text-[1.5rem] font-bold text-[#2D3149]">Двухфакторная аутентификация</h2>
          
          <div v-if="tfaError" class="p-[1rem] bg-red-50 text-red-600 rounded-[1rem] text-[0.9375rem] font-medium">{{ tfaError }}</div>
          <div v-if="tfaSuccess" class="p-[1rem] bg-green-50 text-green-600 rounded-[1rem] text-[0.9375rem] font-medium">{{ tfaSuccess }}</div>

          <div v-if="is2faEnabled" class="space-y-[1.5rem]">
            <div class="p-[1.25rem] bg-green-50 text-green-700 rounded-[1.5rem] text-[0.9375rem] font-medium flex items-center gap-3 border border-green-100">
              <i class="fa-solid fa-circle-check text-xl"></i>
              2FA успешно включена. Ваш аккаунт защищен.
            </div>
          </div>

          <div v-else-if="setupData" class="space-y-[1.5rem]">
            <div class="p-[1.5rem] bg-[#f9f9fa] rounded-[1.5rem] border border-gray-100">
              <h3 class="font-bold text-[#2D3149] mb-2">1. Отсканируйте QR-код</h3>
              <p class="text-[0.875rem] text-black/60 mb-4">Используйте Google Authenticator или Authy.</p>
              <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(setupData.otpauth_uri)}`" alt="QR Code" class="mx-auto mb-4 border border-gray-200 p-3 bg-white rounded-2xl shadow-sm" />
            </div>

            <div class="p-[1.5rem] bg-[#f9f9fa] rounded-[1.5rem] border border-gray-100">
              <h3 class="font-bold text-[#2D3149] mb-2">2. Коды восстановления</h3>
              <p class="text-[0.875rem] text-black/60 mb-4">Сохраните эти коды в надежном месте.</p>
              <div class="grid grid-cols-2 gap-3 font-mono text-[0.875rem] bg-white p-4 border border-gray-200 rounded-xl">
                <div v-for="(code, idx) in setupData.recovery_codes" :key="idx" class="text-center font-bold text-[#2D3149] tracking-wider">{{ code }}</div>
              </div>
            </div>

            <div class="p-[1.5rem] bg-[#f9f9fa] rounded-[1.5rem] border border-gray-100">
              <h3 class="font-bold text-[#2D3149] mb-4">3. Подтвердите активацию</h3>
              <div class="flex flex-col sm:flex-row gap-4">
                <input 
                  v-model="confirmCode" 
                  type="text" 
                  placeholder="000000" 
                  class="input-base text-center sm:text-left tracking-[0.2em] flex-1 font-bold"
                />
                <button @click="confirm2fa" class="btn-primary sm:w-auto px-[2rem]">
                  Активировать
                </button>
              </div>
            </div>
          </div>

          <div v-else class="space-y-[1.5rem]">
            <div class="p-[1.5rem] bg-[#f9f9fa] text-[#2D3149] rounded-[1.5rem] text-[0.9375rem] border border-gray-100">
              Дополнительный уровень безопасности: при входе потребуется ввести код из приложения-аутентификатора.
            </div>
            <button @click="init2fa" class="btn-primary w-full md:w-auto px-[2rem]">
              Настроить 2FA
            </button>
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

const pwdForm = ref({ old_password: '', new_password: '', confirm_password: '' })
const pwdError = ref('')
const pwdSuccess = ref('')
const pwdLoading = ref(false)

const tfaError = ref('')
const tfaSuccess = ref('')
const setupData = ref<any>(null)
const confirmCode = ref('')
const is2faEnabled = ref(false)

onMounted(async () => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/login')
      return
    }
    
    try {
      const res = await fetch('/api/v1/users/me', { headers: { 'Authorization': `Bearer ${token}` } })
      if(res.ok) {
        const data = await res.json()
        is2faEnabled.value = data.is_2fa_enabled || false
      }
    } catch (e) {
      console.error(e)
    }
  }
})

const changePassword = async () => {
  pwdError.value = ''
  pwdSuccess.value = ''
  
  if (pwdForm.value.new_password !== pwdForm.value.confirm_password) {
     pwdError.value = 'Новые пароли не совпадают'
     return
  }
  
  pwdLoading.value = true
  try {
     const token = localStorage.getItem('access_token')
     const res = await fetch('/api/v1/users/me/password', {
       method: 'PUT',
       headers: { 
         'Content-Type': 'application/json',
         'Authorization': `Bearer ${token}` 
       },
       body: JSON.stringify({
         current_password: pwdForm.value.old_password,
         new_password: pwdForm.value.new_password
       })
     })
     
     if (!res.ok) {
       const err = await res.json()
       throw new Error(err.detail || 'Ошибка смены пароля')
     }
     
     pwdSuccess.value = 'Пароль успешно изменен'
     pwdForm.value = { old_password: '', new_password: '', confirm_password: '' }
  } catch (err: any) {
     pwdError.value = err.message || 'Не удалось сменить пароль'
  } finally {
     pwdLoading.value = false
  }
}

const init2fa = async () => {
  tfaError.value = ''
  try {
    const res = await authApi.enable2fa()
    setupData.value = res
  } catch (err: any) {
    tfaError.value = err.detail || 'Ошибка при генерации 2FA.'
  }
}

const confirm2fa = async () => {
  tfaError.value = ''
  const cleanCode = confirmCode.value.replace(/[^a-zA-Z0-9]/g, '')
  if (!cleanCode) return
  
  try {
    await authApi.confirm2fa(cleanCode)
    tfaSuccess.value = 'Двухфакторная аутентификация успешно включена!'
    setupData.value = null
    is2faEnabled.value = true
  } catch (err: any) {
    tfaError.value = err.detail || 'Неверный код подтверждения.'
  }
}
</script>
