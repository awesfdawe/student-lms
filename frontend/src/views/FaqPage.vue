<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto min-h-[calc(100vh-5.625rem)]"
    >
      <h1
        class="font-geologica font-bold text-[2.5rem] md:text-[4rem] text-black mb-[3rem] animate-fade-up"
      >
        Частые вопросы
      </h1>
      <div class="flex flex-col gap-[1.5rem] animate-fade-up" style="animation-delay: 0.2s">
        <div
          class="bg-white/50 backdrop-blur-md rounded-[2rem] p-[2rem] shadow-sm border border-gray-100"
        >
          <h3 class="font-geologica font-bold text-[1.25rem] md:text-[1.5rem] text-black">
            Как проходит обучение?
          </h3>
          <p class="font-roboto text-[1rem] md:text-[1.125rem] text-black/70 mt-[1rem]">
            Обучение проходит онлайн на нашей платформе. Ты смотришь видеоуроки в удобное время,
            выполняешь практические задания и получаешь развернутую обратную связь от персонального
            наставника.
          </p>
        </div>
        <div
          class="bg-white/50 backdrop-blur-md rounded-[2rem] p-[2rem] shadow-sm border border-gray-100"
        >
          <h3 class="font-geologica font-bold text-[1.25rem] md:text-[1.5rem] text-black">
            Есть ли помощь с трудоустройством?
          </h3>
          <p class="font-roboto text-[1rem] md:text-[1.125rem] text-black/70 mt-[1rem]">
            Да, наш карьерный центр помогает составить грамотное резюме, собрать сильное портфолио
            из проектов курса и подготовиться к техническим собеседованиям.
          </p>
        </div>
        <div
          class="bg-white/50 backdrop-blur-md rounded-[2rem] p-[2rem] shadow-sm border border-gray-100"
        >
          <h3 class="font-geologica font-bold text-[1.25rem] md:text-[1.5rem] text-black">
            Можно ли совмещать учебу с работой?
          </h3>
          <p class="font-roboto text-[1rem] md:text-[1.125rem] text-black/70 mt-[1rem]">
            Конечно! Расписание гибкое. Ты сам выбираешь темп прохождения модулей. В среднем для
            комфортного обучения достаточно уделять от 1 до 2 часов в день.
          </p>
        </div>
      </div>
      <div
        class="flex flex-wrap items-center gap-[1rem] mt-[3rem] w-full max-w-[30rem] animate-fade-up"
        style="animation-delay: 0.3s"
      >
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
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'

const router = useRouter()
</script>
