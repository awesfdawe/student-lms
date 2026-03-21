<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[60rem] mx-auto min-h-[calc(100vh-5.625rem)]"
    >
      <h1
        class="font-geologica font-bold text-[2.5rem] md:text-[3.5rem] text-black mb-[2rem] animate-fade-up"
      >
        Политика конфиденциальности
      </h1>
      <div
        class="prose prose-lg prose-blue max-w-none font-roboto text-black/80 animate-fade-up"
        style="animation-delay: 0.1s"
      >
        <p class="mb-4"><strong>1. Общие положения</strong></p>
        <p class="mb-4">
          Настоящая политика обработки персональных данных составлена в соответствии с требованиями
          Федерального закона от 27.07.2006. №152-ФЗ «О персональных данных» и определяет порядок
          обработки персональных данных и меры по обеспечению безопасности персональных данных,
          предпринимаемые ООО "СКИЛЛФОРДЖ".
        </p>
        <p class="mb-4"><strong>2. Основные понятия, используемые в Политике</strong></p>
        <ul class="list-disc pl-5 mb-4 space-y-2">
          <li>
            <strong>Веб-сайт</strong> — совокупность графических и информационных материалов, а
            также программ для ЭВМ и баз данных, обеспечивающих их доступность в сети интернет по
            сетевому адресу skillforge.ru;
          </li>
          <li><strong>Пользователь</strong> — любой посетитель веб-сайта;</li>
          <li>
            <strong>Персональные данные</strong> — любая информация, относящаяся прямо или косвенно
            к определенному или определяемому Пользователю веб-сайта.
          </li>
        </ul>
      </div>
      <div class="flex flex-wrap gap-[1rem] mt-[3rem]">
        <button @click="router.back()" class="btn-cta !bg-gray-200 !text-black hover:!bg-gray-300">
          Назад
        </button>
        <router-link to="/" class="btn-cta"> На главную </router-link>
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'

const router = useRouter()
</script>
