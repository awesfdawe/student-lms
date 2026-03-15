<template>
  <router-link to="#test" :class="['btn-cta', fullWidth ? '!w-full' : '']" @click="$emit('click')">
    {{ text }}
  </router-link>
</template>

<script setup lang="ts">
interface Props {
  text?: string
  fullWidth?: boolean
}

withDefaults(defineProps<Props>(), {
  text: 'Записаться на курс',
  fullWidth: false,
})

defineEmits(['click'])
</script>
