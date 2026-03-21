<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] max-w-[30rem] mx-auto min-h-[calc(100vh-5.625rem)] flex flex-col justify-center animate-fade-up"
    >
      <h1
        class="font-geologica font-bold text-[2rem] md:text-[2.5rem] text-black mb-[1rem] text-center"
      >
        Вход в систему
      </h1>
      <p class="font-roboto text-black/70 text-center mb-[2rem]">
        С возвращением! Пожалуйста, введите свои данные.
      </p>

      <form @submit.prevent="handleLogin" class="flex flex-col gap-[1.25rem]">
        <div class="flex flex-col gap-[0.5rem]">
          <label class="font-roboto text-[0.9375rem] font-bold text-black">Email</label>
          <input
            type="email"
            required
            placeholder="Введите ваш email"
            class="w-full h-[3.5rem] px-[1.25rem] rounded-[1rem] border border-gray-200 bg-white/50 focus:bg-white focus:border-accent outline-none transition-colors font-roboto text-[1rem]"
          />
        </div>
        <div class="flex flex-col gap-[0.5rem]">
          <label class="font-roboto text-[0.9375rem] font-bold text-black">Пароль</label>
          <input
            type="password"
            required
            placeholder="Введите пароль"
            class="w-full h-[3.5rem] px-[1.25rem] rounded-[1rem] border border-gray-200 bg-white/50 focus:bg-white focus:border-accent outline-none transition-colors font-roboto text-[1rem]"
          />
        </div>
        <button type="submit" class="btn-cta w-full mt-[1rem]">Войти</button>
      </form>

      <div class="mt-[2rem] text-center font-roboto text-[0.9375rem] text-black/70">
        Нет аккаунта?
        <router-link to="/register" class="text-accent font-bold hover:underline"
          >Зарегистрируйтесь</router-link
        >
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'

const handleLogin = () => {
  console.log('Login attempt')
  // Здесь будет логика работы с API
}
</script>
