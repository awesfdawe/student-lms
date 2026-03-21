<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto min-h-[calc(100vh-5.625rem)] flex flex-col justify-center"
    >
      <div class="max-w-[60rem] animate-fade-up">
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
            Наша миссия — помочь тебе найти свой путь в IT и digital-сфере. Мы не просто даем сухую
            теорию, мы обеспечиваем актуальные знания, круглосуточную поддержку наставников и
            реальную практику на проектах, которые не стыдно показать работодателю.
          </p>
        </div>

        <div
          class="mt-[3rem] p-[2rem] bg-white/50 backdrop-blur-md rounded-[2rem] border border-gray-100"
        >
          <h2 class="font-geologica font-bold text-[1.5rem] md:text-[2rem] text-black mb-[1rem]">
            Правовая информация
          </h2>
          <ul class="flex flex-col gap-[1rem] font-roboto text-[1.125rem] text-black/80">
            <li>
              <router-link to="/privacy" class="text-accent hover:underline font-bold"
                >Политика конфиденциальности</router-link
              >
              — узнай, как мы бережно храним и обрабатываем твои персональные данные.
            </li>
            <li>
              <router-link to="/terms" class="text-accent hover:underline font-bold"
                >Публичная оферта</router-link
              >
              — официальный договор на оказание образовательных услуг и предоставление доступа к
              платформе.
            </li>
            <li>
              <span class="text-black font-bold">Государственная лицензия:</span> №
              Л035-01298-77/00181484 от 15.03.2026 г. Мы имеем официальное право на ведение
              образовательной деятельности.
            </li>
          </ul>
        </div>

        <div class="flex flex-wrap items-center gap-[1rem] mt-[3rem] w-full max-w-[40rem]">
          <button
            @click="router.back()"
            class="btn-cta !bg-gray-200 !text-black hover:!bg-gray-300 flex-grow whitespace-nowrap text-center"
          >
            Назад
          </button>
          <router-link
            to="/contacts"
            class="btn-cta !bg-transparent !text-black border-2 border-accent hover:!bg-accent hover:!text-white flex-grow whitespace-nowrap text-center"
          >
            Наши контакты
          </router-link>
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
