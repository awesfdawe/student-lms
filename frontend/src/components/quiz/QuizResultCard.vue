<template>
  <div class="flex flex-col gap-[2rem] p-2">
    <div
      class="bg-[#2D3149]/38 rounded-[3rem] p-[2rem] min-h-[9.3125rem] flex flex-col items-center justify-center gap-2 text-center"
    >
      <h3 class="font-geologica text-white text-[1.5rem] md:text-[1.75rem] font-bold">
        Ваш план готов!
      </h3>
      <p class="font-geologica text-white text-[1rem]">Основан на вашем опыте</p>
    </div>
    <div class="bg-white/70 backdrop-blur-sm rounded-[2rem] p-6 text-left shadow-inner">
      <p class="font-roboto text-[1.125rem] leading-[1.6] text-black">
        {{ resultText }}
      </p>
    </div>
    <div class="flex flex-col gap-[1rem] mt-2">
      <button class="btn-cta w-full">Получить полную программу</button>
      <button
        @click="$emit('reset')"
        class="w-full h-[3.5rem] flex items-center justify-center font-geologica font-bold text-[0.9375rem] text-white/80 hover:text-white transition-colors cursor-pointer"
      >
        Пройти заново
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ resultText: string }>()
defineEmits<{ (e: 'reset'): void }>()
</script>
