import { defineStore } from 'pinia'
import { API_BASE_URL } from '@/api'

export const useCmsStore = defineStore('cms', {
  state: () => ({
    content: {} as Record<string, any>
  }),
  actions: {
    async fetchCollection(collection: string) {
      if (this.content[collection]) return
      try {
        const res = await fetch(`${API_BASE_URL}/cms/${collection}`)
        if (res.ok) {
          this.content[collection] = await res.json()
        }
      } catch (e) {
      }
    }
  }
})
