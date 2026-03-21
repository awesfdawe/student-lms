<template>
  <section class="relative z-10 pt-[5rem] md:pt-[10rem] pb-[3rem] md:pb-[6rem] layout-container">
    <div
      ref="sectionRef"
      class="grid grid-cols-1 lg:grid-cols-2 gap-[1.5rem] md:gap-[2.5rem] transition-all duration-1000 transform"
      :class="isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-[3rem]'"
    >
      <div class="flex flex-col justify-center mb-[2rem] lg:mb-0">
        <CoursesTitle />
      </div>

      <CourseCard
        title="UX/UI дизайнер"
        duration="3 месяца"
        feature="помощь в трудоустройстве"
        image="/src/assets/images/course-ux-ui.jpg"
        link="/course/ux-ui"
      />

      <CourseCard
        title="Программист"
        duration="6 месяцев"
        feature="помощь в трудоустройстве"
        image="/src/assets/images/course-programmer.jpg"
        link="/course/programmer"
      />

      <CourseCard
        title="3D-дизайнер"
        duration="3 месяца"
        feature="помощь в трудоустройстве"
        image="/src/assets/images/course-3d.jpg"
        link="/course/3d-designer"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import CoursesTitle from './CoursesTitle.vue'
import CourseCard from './CourseCard.vue'

const sectionRef = ref<HTMLElement | null>(null)
const isVisible = ref(false)
let observer: IntersectionObserver | null = null

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      const entry = entries[0]
      if (entry?.isIntersecting) {
        isVisible.value = true
        if (sectionRef.value) observer?.unobserve(sectionRef.value)
      }
    },
    { threshold: 0.1 },
  )

  if (sectionRef.value) {
    observer.observe(sectionRef.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>
