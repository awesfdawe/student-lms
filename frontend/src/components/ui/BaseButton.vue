<script setup lang="ts">
import { computed } from 'vue';
import { useCmsStore } from '@/stores/cms';

const props = defineProps<{
  dictKey?: string;
  variant?: 'primary' | 'secondary';
  to?: string;
}>();

const cmsStore = useCmsStore();
const buttonText = computed(() => {
  const item = cmsStore.content['ui_dictionary']?.find((i: any) => i.key === props.dictKey);
  return item ? item.value : '';
});
</script>

<template>
  <component
    :is="to ? 'router-link' : 'button'"
    :to="to"
    :class="['btn', `btn-${variant || 'primary'}`]"
  >
    <template v-if="buttonText">{{ buttonText }}</template>
    <slot v-else />
  </component>
</template>
