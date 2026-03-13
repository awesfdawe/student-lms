<template>
  <a href="#test" class="btn-cta">
    {{ text }}
  </a>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: "Записаться на курс"
  }
})
</script>