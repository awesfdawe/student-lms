<template>
  <div
    v-if="!isAccepted"
    class="fixed bottom-0 left-0 right-0 bg-white shadow-[0_-10px_40px_rgba(0,0,0,0.1)] z-[100] border-t border-gray-100 p-[1.5rem] sm:p-[2rem]"
  >
    <div
      class="max-w-[80rem] mx-auto flex flex-col sm:flex-row items-center justify-between gap-[1.5rem]"
    >
      <div
        class="font-roboto text-[0.9375rem] text-black/80 text-center sm:text-left leading-relaxed max-w-[50rem]"
      >
        Мы используем файлы cookie, чтобы улучшить работу сайта и сделать его удобнее для вас.
        Продолжая использовать сайт, вы даете согласие на сбор данных в соответствии с
        <router-link to="/privacy" class="text-accent hover:underline font-bold"
          >Политикой конфиденциальности</router-link
        >.
      </div>
      <button @click="acceptCookies" class="btn-cta whitespace-nowrap !py-[0.75rem] !px-[2rem]">
        Понятно, спасибо
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isAccepted = ref(true)

onMounted(() => {
  if (!localStorage.getItem('cookie_consent')) {
    isAccepted.value = false
  }
})

const acceptCookies = () => {
  localStorage.setItem('cookie_consent', 'true')
  isAccepted.value = true
}
</script>
