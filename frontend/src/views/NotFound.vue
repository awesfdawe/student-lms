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
        Кажется, вы заблудились. Запрашиваемая страница была удалена или перенесена по другому
        адресу.
      </p>
      <router-link to="/" class="btn-cta"> На главную </router-link>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
</script>
