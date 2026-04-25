import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<any>(null);
  const token = ref<string | null>(localStorage.getItem('access_token') || null);

  const isAuthenticated = computed(() => !!token.value);

  const setToken = (newToken: string) => {
    token.value = newToken;
    localStorage.setItem('access_token', newToken);
  };

  const logout = () => {
    user.value = null;
    token.value = null;
    localStorage.removeItem('access_token');
  };

  return {
    user,
    token,
    isAuthenticated,
    setToken,
    logout,
  };
});
