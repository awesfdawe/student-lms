<template>
  <section class="py-[4rem] md:py-[6rem] bg-white relative z-10">
    <div class="layout-container">
      <CoursesTitle />
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-[1.5rem] md:gap-[2.5rem] mt-12 animate-fade-up">
        <CourseCard
          v-for="course in displayCourses"
          :key="course.id"
          :title="course.title"
          :duration="course.duration"
          :feature="course.feature"
          :image="course.image || '/src/assets/images/course-programmer.jpg'"
          :link="'/course/' + course.slug"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onServerPrefetch, onMounted } from 'vue'
import CoursesTitle from './CoursesTitle.vue'
import CourseCard from './CourseCard.vue'
import { useContent } from '@/composables/useContent'

const { fetchCourses, courseList } = useContent()

const displayCourses = computed(() => {
  const list = Array.isArray(courseList.value) ? courseList.value : []
  return list.filter((c: any) => c !== null && c !== undefined)
})

const loadData = async () => {
  await fetchCourses()
}

onServerPrefetch(loadData)

onMounted(() => {
  if (!courseList.value || courseList.value.length === 0) {
    loadData()
  }
})
</script>
