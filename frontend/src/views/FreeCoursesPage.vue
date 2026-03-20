<template>
  <MainLayout>
    <section
      class="relative z-10 pt-[7rem] md:pt-[10rem] pb-[5rem] px-[1.25rem] xl:px-[5.625rem] max-w-[80rem] mx-auto min-h-[calc(100vh-5.625rem)]"
    >
      <h1
        class="font-geologica font-bold text-[2.5rem] md:text-[4rem] text-black mb-[1rem] animate-fade-up"
      >
        Бесплатные курсы
      </h1>
      <p
        class="font-roboto text-[1.125rem] text-black/70 mb-[3rem] animate-fade-up max-w-[40rem]"
        style="animation-delay: 0.1s"
      >
        Попробуйте наши вводные программы абсолютно бесплатно, чтобы понять, какое IT-направление
        подходит вам больше всего, прежде чем принимать решение.
      </p>
      <div
        class="grid grid-cols-1 lg:grid-cols-2 gap-[1.5rem] md:gap-[2.5rem] animate-fade-up"
        style="animation-delay: 0.2s"
      >
        <CourseCard
          title="Основы дизайна"
          duration="1 неделя"
          feature="вводный курс"
          image="/src/assets/images/course-ux-ui.jpg"
          link="/course/ux-ui"
        />
        <CourseCard
          title="Введение в код"
          duration="2 недели"
          feature="вводный курс"
          image="/src/assets/images/course-programmer.jpg"
          link="/course/programmer"
        />
      </div>
    </section>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/layout/MainLayout.vue'
import CourseCard from '@/components/courses/CourseCard.vue'
</script>
