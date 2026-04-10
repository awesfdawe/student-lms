import { defineStore } from 'pinia'

export const useFaqStore = defineStore('faq', {
  state: () => ({
    items: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchFaqs() {
      if (this.items.length > 0) return
      this.loading = true
      try {
        const base = import.meta.env.SSR ? (process.env.API_URL || 'http://backend:8000') : ''
        const res = await fetch(`${base}/api/v1/cms/faq`)
        if (!res.ok) throw new Error('API Error')
        const data = await res.json()
        this.items = data
      } catch (e) {
        this.error = e.message || 'Error'
      } finally {
        this.loading = false
      }
    }
  }
})
