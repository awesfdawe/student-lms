<template>
  <MainLayout>
    <section
      class="flex flex-col items-center justify-center min-h-[calc(100vh-5.625rem)] text-center px-[1.25rem] animate-fade-up pt-[10%] pb-[5%]"
    >
      <div class="relative">
        <div class="absolute inset-0 bg-accent/20 blur-3xl rounded-full scale-150"></div>
        <h1
          class="relative font-geologica font-bold text-[8rem] md:text-[12rem] leading-none text-accent"
        >
          404
        </h1>
      </div>
      <h2 class="font-geologica font-bold text-[2rem] md:text-[3rem] mt-[1rem] text-black">
        Страница не найдена
      </h2>
      <p class="font-roboto text-[1.125rem] text-black/70 mt-[1rem] mb-[3rem] max-w-[25rem]">
        Кажется, ты заблудился. Запрашиваемая страница была удалена или перенесена по другому
        адресу.
      </p>
      <div class="flex flex-wrap items-center justify-center gap-[1rem] w-full max-w-[30rem]">
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
