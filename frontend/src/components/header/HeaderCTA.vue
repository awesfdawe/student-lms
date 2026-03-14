<template>
  <router-link to="#test" class="btn-cta">
    {{ text }}
  </router-link>
</template>

<script setup lang="ts">
interface Props {
  text?: string
}

withDefaults(defineProps<Props>(), {
  text: 'Записаться на курс',
})
</script>
