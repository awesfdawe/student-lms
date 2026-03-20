<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto min-h-[calc(100vh-5.625rem)] flex flex-col justify-center"
    >
      <div class="max-w-[50rem] animate-fade-up">
        <h1 class="font-geologica font-bold text-[2.5rem] md:text-[4rem] text-black mb-[2rem]">
          О нас
        </h1>
        <div class="flex flex-col gap-[1.5rem]">
          <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black/80 leading-[1.6]">
            <b class="text-black">SKILLFORGE</b> — это образовательная платформа нового поколения.
            Мы верим, что современные технологии и искусственный интеллект способны сделать обучение
            профессиям будущего доступным, быстрым и максимально эффективным для каждого.
          </p>
          <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black/80 leading-[1.6]">
            Наша миссия — помочь вам найти свой путь в IT и digital-сфере. Мы не просто даем сухую
            теорию, мы обеспечиваем актуальные знания, круглосуточную поддержку наставников и
            реальную практику на проектах, которые не стыдно показать работодателю.
          </p>
        </div>
        <router-link to="/" class="btn-cta mt-[3rem]"> На главную </router-link>
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
</script>
