<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] max-w-[35rem] mx-auto min-h-[calc(100vh-5.625rem)] flex flex-col justify-center animate-fade-up"
    >
      <h1
        class="font-geologica font-bold text-[2rem] md:text-[2.5rem] text-black mb-[1rem] text-center"
      >
        Регистрация
      </h1>
      <p class="font-roboto text-black/70 text-center mb-[2rem]">
        Создайте аккаунт, чтобы начать обучение
      </p>

      <form @submit.prevent="handleRegister" class="flex flex-col gap-[1.25rem]">
        <div class="flex flex-col gap-[0.5rem]">
          <label class="font-roboto text-[0.9375rem] font-bold text-black">Имя и Фамилия</label>
          <input
            type="text"
            required
            placeholder="Иван Иванов"
            class="w-full h-[3.5rem] px-[1.25rem] rounded-[1rem] border border-gray-200 bg-white/50 focus:bg-white focus:border-accent outline-none transition-colors font-roboto text-[1rem]"
          />
        </div>
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
            placeholder="Придумайте надежный пароль"
            class="w-full h-[3.5rem] px-[1.25rem] rounded-[1rem] border border-gray-200 bg-white/50 focus:bg-white focus:border-accent outline-none transition-colors font-roboto text-[1rem]"
          />
        </div>

        <div class="flex flex-col gap-[1rem] mt-[1rem]">
          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              type="checkbox"
              required
              class="mt-1 w-[1.25rem] h-[1.25rem] accent-accent cursor-pointer"
            />
            <span
              class="font-roboto text-[0.875rem] text-black/70 group-hover:text-black transition-colors leading-tight"
            >
              Я даю согласие на обработку моих персональных данных в соответствии с
              <router-link to="/privacy" class="text-accent hover:underline"
                >Политикой конфиденциальности</router-link
              >
              и принимаю условия
              <router-link to="/terms" class="text-accent hover:underline"
                >Публичной оферты</router-link
              >
              (обязательно).
            </span>
          </label>
          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              type="checkbox"
              class="mt-1 w-[1.25rem] h-[1.25rem] accent-accent cursor-pointer"
            />
            <span
              class="font-roboto text-[0.875rem] text-black/70 group-hover:text-black transition-colors leading-tight"
            >
              Я хочу получать информацию о новых курсах, акциях и специальных предложениях на мой
              email.
            </span>
          </label>
        </div>

        <button type="submit" class="btn-cta w-full mt-[1rem]">Зарегистрироваться</button>
      </form>

      <div class="mt-[2rem] text-center font-roboto text-[0.9375rem] text-black/70">
        Уже есть аккаунт?
        <router-link to="/login" class="text-accent font-bold hover:underline">Войти</router-link>
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'

const handleRegister = () => {
  console.log('Registration attempt')
  // Здесь будет логика работы с API
}
</script>
