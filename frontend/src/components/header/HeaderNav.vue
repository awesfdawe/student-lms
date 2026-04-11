<template>
  <nav :class="[isMobile ? 'flex flex-col w-full gap-[2rem] text-center' : 'hidden lg:flex gap-[2rem] xl:gap-[3rem] items-center']">
    <router-link to="/free" class="nav-link" @click="$emit('close')">{{ t('header_nav_free') }}</router-link>
    <router-link to="/about" class="nav-link" @click="$emit('close')">{{ t('header_nav_about') }}</router-link>
    <router-link to="/contacts" class="nav-link" @click="$emit('close')">{{ t('header_nav_contacts') }}</router-link>
    <router-link to="/faq" class="nav-link" @click="$emit('close')">{{ t('header_nav_faq') }}</router-link>
  </nav>
</template>

<script setup lang="ts">
import { useContent } from '@/composables/useContent'
defineProps<{ isMobile?: boolean }>()
defineEmits(['close'])
const { t } = useContent()
</script>
