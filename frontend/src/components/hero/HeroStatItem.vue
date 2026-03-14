<template>
  <div class="flex flex-col items-center text-center space-y-4">
    <div
      class="bg-white/50 backdrop-blur-sm rounded-[1.75rem] px-6 min-w-[10.75rem] h-[2.6875rem] flex items-center justify-center"
    >
      <span
        :class="[
          'font-geologica text-[2rem] leading-none text-black',
          isBoldValue ? 'font-extrabold' : 'font-bold',
        ]"
      >
        {{ value }}
      </span>
    </div>

    <p class="font-roboto text-[1.25rem] leading-tight text-black max-w-[15.4375rem]">
      {{ description }}
    </p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  value: string
  description: string
  isBoldValue?: boolean
}

withDefaults(defineProps<Props>(), {
  isBoldValue: true,
})
</script>