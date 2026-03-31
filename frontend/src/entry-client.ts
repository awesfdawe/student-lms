import { createApp } from './main'

const { app, router, pinia } = createApp()

declare global {
  interface Window {
    __INITIAL_STATE__?: any;
  }
}

if (window.__INITIAL_STATE__) {
  pinia.state.value = window.__INITIAL_STATE__
}

router.isReady().then(() => {
  app.mount('#app') 
})
