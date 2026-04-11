<template>
  <div :class="['flex items-center', fullWidth ? 'flex-col w-full gap-[1.5rem]' : 'gap-[1.5rem]']">
    <template v-if="isAuthenticated">
      <router-link to="/profile" :class="[fullWidth ? 'w-full text-center py-[1rem]' : '', 'nav-link']" @click="$emit('click')">Мой кабинет</router-link>
      <button @click="handleLogout" :class="['btn-cta text-[0.9375rem]', fullWidth ? 'w-full' : 'px-[1.5rem]']">Выйти</button>
    </template>
    <template v-else>
      <router-link to="/login" :class="[fullWidth ? 'w-full text-center py-[1rem]' : '', 'nav-link']" @click="$emit('click')">{{ t('header_cta_login', 'Войти') }}</router-link>
      <router-link to="/register" :class="['btn-cta text-[0.9375rem]', fullWidth ? 'w-full' : 'px-[1.5rem]']" @click="$emit('click')">{{ t('header_cta_register', 'Регистрация') }}</router-link>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useContent } from '@/composables/useContent'

defineProps<{ fullWidth?: boolean }>()
const emit = defineEmits(['click'])
const { t } = useContent()
const router = useRouter()
const isAuthenticated = ref(false)

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('access_token')
})

const handleLogout = () => {
  localStorage.removeItem('access_token')
  isAuthenticated.value = false
  emit('click')
  router.push('/')
}
</script>
