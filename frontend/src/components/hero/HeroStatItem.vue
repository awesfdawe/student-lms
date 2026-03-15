<template>
  <div
    class="flex flex-col items-start md:items-center text-left md:text-center space-y-[0.5rem] md:space-y-[1rem] bg-white/40 md:bg-transparent backdrop-blur-md md:backdrop-blur-none p-[1.25rem] md:p-0 rounded-[1.5rem] border border-white/60 md:border-none shadow-sm md:shadow-none hover:shadow-md md:hover:shadow-none transition-shadow duration-300"
  >
    <div
      class="md:bg-white/50 md:backdrop-blur-sm rounded-[1.75rem] md:px-6 md:py-2 md:min-w-[10.75rem] md:h-[2.6875rem] flex items-center justify-start md:justify-center"
    >
      <span
        :class="[
          'font-geologica text-[1.5rem] whitespace-nowrap md:text-[2rem] leading-none text-black',
          isBoldValue ? 'font-extrabold' : 'font-bold',
        ]"
      >
        {{ value }}
      </span>
    </div>

    <p
      class="font-roboto text-[0.9375rem] md:text-[1.25rem] leading-tight text-black max-w-[15.4375rem]"
    >
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
