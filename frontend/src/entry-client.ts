import { createApp } from './main'

const { app, router, pinia } = createApp()

if (window.__INITIAL_STATE__) {
  pinia.state.value = window.__INITIAL_STATE__
}

router.isReady().then(() => {
  app.mount('#app')
})
