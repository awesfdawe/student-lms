import { renderToString } from 'vue/server-renderer'
import { createApp } from './main'

export async function render(url: string) {
  const { app, router, pinia } = createApp()

  await router.push(url)
  await router.isReady()

  const matchedComponents = router.currentRoute.value.matched.flatMap(record =>
    Object.values(record.components || {})
  )

  await Promise.all(
    matchedComponents.map(async component => {
      if (typeof component === 'function') {
        const mod = await component()
        return mod.default || mod
      }
      return component
    })
  )

  const html = await renderToString(app)
  const state = pinia.state.value

  return { html, state }
}
