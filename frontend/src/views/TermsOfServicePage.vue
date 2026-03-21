<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[60rem] mx-auto min-h-[calc(100vh-5.625rem)]"
    >
      <h1
        class="font-geologica font-bold text-[2.5rem] md:text-[3.5rem] text-black mb-[2rem] animate-fade-up"
      >
        Публичная оферта
      </h1>
      <div
        class="prose prose-lg prose-blue max-w-none font-roboto text-black/80 animate-fade-up"
        style="animation-delay: 0.1s"
      >
        <p class="mb-4"><strong>1. Предмет договора</strong></p>
        <p class="mb-4">
          Настоящий документ является публичной офертой ООО "СКИЛЛФОРДЖ" в соответствии со ст. 437
          Гражданского кодекса РФ. Оферта определяет условия предоставления платного доступа к
          образовательным материалам (курсам, программам ДПО) посредством Платформы.
        </p>
        <p class="mb-4"><strong>2. Условия оказания услуг и доступ</strong></p>
        <p class="mb-4">
          Доступ к образовательным материалам предоставляется Пользователю после прохождения
          процедуры регистрации и 100% предоплаты стоимости выбранного курса (если не указано иное,
          например, при покупке в рассрочку через банки-партнеры).
        </p>
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
