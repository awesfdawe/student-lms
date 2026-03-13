<template>
  <div class="flex flex-col items-center text-center space-y-4">
    <div class="bg-white/50 backdrop-blur-sm rounded-[28px] px-6 min-w-[172px] h-[43px] flex items-center justify-center">
      <span 
        :class="[
          'font-geologica text-[32px] leading-none text-black',
          isBoldValue ? 'font-extrabold' : 'font-bold'
        ]"
      >
        {{ value }}
      </span>
    </div>
    
    <p class="font-roboto text-[20px] leading-tight text-black max-w-[247px]">
      {{ description }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  value: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  isBoldValue: {
    type: Boolean,
    default: true
  }
})
</script>