<template>
  <a href="#test" class="btn-cta">
    {{ text }}
  </a>
</template>

<script setup lang="ts">
interface Props {
  text?: string
}

withDefaults(defineProps<Props>(), {
  text: 'Записаться на курс',
})
</script>