<template>
  <MainLayout>
    <section
      class="relative z-10 flex flex-col justify-center min-h-[calc(100vh-5.625rem)] pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto mt-[5.625rem] md:mt-0"
    >
      <div
        v-if="course"
        class="flex flex-col-reverse lg:flex-row items-center justify-between gap-[3rem] lg:gap-[5rem] animate-fade-up w-full"
      >
        <div class="w-full lg:w-1/2 flex flex-col items-start gap-[1.5rem]">
          <h1
            class="font-geologica font-bold text-[2.5rem] md:text-[4rem] leading-[1.1] text-black"
          >
            {{ course.title }}
          </h1>
          <div class="flex flex-col gap-2">
            <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black/80">
              Длительность: <b class="text-black">{{ course.duration }}</b>
            </p>
            <p class="font-roboto text-[1.125rem] md:text-[1.25rem] text-black/80">
              Преимущество: <b class="text-black">{{ course.feature }}</b>
            </p>
          </div>
          <p
            class="font-roboto text-[1rem] md:text-[1.125rem] leading-[1.6] text-black/70 max-w-[34.375rem]"
          >
            Освойте одну из самых востребованных профессий с нуля. Мы подготовили для вас
            интенсивную программу с упором на практику, помощь наставников и формирование сильного
            портфолио для быстрого старта карьеры.
          </p>
          <router-link to="/#test" class="btn-cta mt-[1rem]"> Записаться на курс </router-link>
        </div>

        <div class="w-full lg:w-1/2 relative group">
          <div
            class="absolute inset-0 bg-accent/20 blur-3xl rounded-full scale-90 group-hover:scale-105 transition-transform duration-700"
          ></div>
          <img
            :src="course.image"
            :alt="course.title"
            class="relative w-full h-auto object-cover rounded-[3.125rem] shadow-2xl aspect-video lg:aspect-[4/3] group-hover:-translate-y-2 transition-transform duration-500"
          />
        </div>
      </div>

      <div
        v-else
        class="flex flex-col items-center justify-center text-center gap-[2rem] w-full animate-fade-up py-[10rem]"
      >
        <h1 class="font-geologica font-bold text-[3rem] md:text-[5rem] text-black leading-none">
          Курс не найден
        </h1>
        <p class="font-roboto text-[1.25rem] text-black/70">
          Возможно, вы перешли по устаревшей ссылке или такого курса пока нет.
        </p>
        <router-link to="/" class="btn-cta"> На главную </router-link>
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/layout/MainLayout.vue'

import uxUiImg from '@/assets/images/course-ux-ui.jpg'
import progImg from '@/assets/images/course-programmer.jpg'
import tdImg from '@/assets/images/course-3d.jpg'

const route = useRoute()
const courseId = route.params.id as string

const coursesInfo: Record<
  string,
  { title: string; duration: string; feature: string; image: string }
> = {
  'ux-ui': {
    title: 'UX/UI дизайнер',
    duration: '3 месяца',
    feature: 'помощь в трудоустройстве',
    image: uxUiImg,
  },
  programmer: {
    title: 'Программист',
    duration: '6 месяцев',
    feature: 'помощь в трудоустройстве',
    image: progImg,
  },
  '3d-designer': {
    title: '3D-дизайнер',
    duration: '3 месяца',
    feature: 'помощь в трудоустройстве',
    image: tdImg,
  },
}

const course = computed(() => coursesInfo[courseId])
</script>
