<template>
  <nav
    aria-label="Основная навигация"
    :class="[
      'font-geologica text-[0.9375rem] flex',
      isMobile ? 'flex-col items-center gap-6' : 'items-center gap-10 xl:gap-[3.75rem]',
    ]"
  >
    <router-link
      v-for="item in navItems"
      :key="item.id"
      :to="item.link"
      class="text-black hover:text-accent transition-colors duration-200"
    >
      {{ item.label }}
    </router-link>
  </nav>
</template>

<script setup lang="ts">
interface Props {
  isMobile?: boolean
}

withDefaults(defineProps<Props>(), {
  isMobile: false,
})

interface NavItem {
  id: string
  label: string
  link: string
}

const navItems: NavItem[] = [
  { id: 'faq', label: 'Частые вопросы', link: '#faq' },
  { id: 'free', label: 'Бесплатные курсы', link: '#free' },
  { id: 'about', label: 'О нас', link: '#about' },
]
</script>
