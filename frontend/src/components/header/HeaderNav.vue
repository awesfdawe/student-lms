<template>
  <nav 
    :class="[
      'font-geologica text-[15px] flex',
      isMobile ? 'flex-col items-center gap-6' : 'items-center gap-10 xl:gap-[60px]'
    ]"
  >
    <a
      v-for="item in navItems"
      :key="item.id"
      :href="item.link"
      class="text-black hover:text-accent transition-colors duration-200"
    >
      {{ item.label }}
    </a>
  </nav>
</template>

<script setup>
defineProps({
  isMobile: {
    type: Boolean,
    default: false
  }
})

const navItems = [
  { id: "faq", label: "Частые вопросы", link: "#faq" },
  { id: "free", label: "Бесплатные курсы", link: "#free" },
  { id: "about", label: "О нас", link: "#about" }
]
</script>