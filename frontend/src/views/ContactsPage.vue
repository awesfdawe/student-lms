<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto min-h-[calc(100vh-5.625rem)] flex flex-col justify-center"
    >
      <div class="max-w-[50rem] animate-fade-up">
        <h1 class="font-geologica font-bold text-[2.5rem] md:text-[4rem] text-black mb-[2rem]">
          Контакты
        </h1>
        <div class="flex flex-col gap-[1.5rem] mb-[3rem]">
          <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black/80 leading-[1.6]">
            Мы всегда на связи и готовы ответить на твои вопросы по поводу обучения, платформы или
            корпоративного сотрудничества.
          </p>
          <div
            class="flex flex-col gap-[1rem] bg-white/50 backdrop-blur-md rounded-[2rem] p-[2rem] shadow-sm border border-gray-100"
          >
            <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black">
              <b class="text-accent">Телефон:</b> +7 (800) 555-35-35
            </p>
            <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black">
              <b class="text-accent">Email:</b> hello@skillforge.ru
            </p>
            <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black">
              <b class="text-accent">Офис:</b> г. Калининград, ул. Брамса 9, кабинет 11
            </p>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-[1rem] w-full max-w-[30rem]">
          <button
            @click="router.back()"
            class="btn-cta !bg-gray-200 !text-black hover:!bg-gray-300 flex-grow whitespace-nowrap text-center"
          >
            Назад
          </button>
          <router-link to="/" class="btn-cta flex-grow-[2] whitespace-nowrap text-center">
            На главную
          </router-link>
        </div>
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'

const router = useRouter()
</script>
