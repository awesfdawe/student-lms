import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import express from 'express'
import Redis from 'ioredis'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const isProduction = process.env.NODE_ENV === 'production'

const redis = new Redis(process.env.REDIS_URL || 'redis://localhost:6379/0')

export async function createServer() {
  const app = express()
  let vite: any

  if (!isProduction) {
    vite = await import('vite').then(m => m.createServer({
      server: { middlewareMode: true },
      appType: 'custom'
    }))
    app.use(vite.middlewares)
  } else {
    const compression = (await import('compression')).default
    const sirv = (await import('serve-static')).default
    app.use(compression())
    app.use(sirv(path.resolve(__dirname, 'dist/client'), { index: false }))
  }

  app.use('*', async (req, res, next) => {
    try {
      const url = req.originalUrl
      
      const publicRoutes = ['/', '/about', '/contacts', '/faq', '/free', '/privacy-policy', '/terms-of-service']
      const isPublicRoute = publicRoutes.includes(url) || url.startsWith('/course/')
      const hasAuthCookie = req.headers.cookie?.includes('access_token')
      
      const shouldCache = isPublicRoute && !hasAuthCookie
      const cacheKey = `ssr_page:${url}`

      if (shouldCache) {
        try {
          const cachedHtml = await redis.get(cacheKey)
          if (cachedHtml) {
            return res.status(200).set({ 'Content-Type': 'text/html' }).end(cachedHtml)
          }
        } catch(err) {
          console.warn("Redis is not available, skipping cache.")
        }
      }

      let template, render
      if (!isProduction) {
        template = fs.readFileSync(path.resolve(__dirname, 'index.html'), 'utf-8')
        template = await vite.transformIndexHtml(url, template)
        render = (await vite.ssrLoadModule('/src/entry-server.ts')).render
      } else {
        template = fs.readFileSync(path.resolve(__dirname, 'dist/client/index.html'), 'utf-8')
        render = (await import('./dist/server/entry-server.js')).render
      }

      const { html: appHtml, state } = await render(url)
      const stateScript = `<script>window.__INITIAL_STATE__=${JSON.stringify(state)}</script>`
      
      const html = template
        .replace('', appHtml)
        .replace('', stateScript)

      if (shouldCache) {
        try {
          await redis.set(cacheKey, html, 'EX', 3600)
        } catch(err) {}
      }

      res.status(200).set({ 'Content-Type': 'text/html' }).end(html)
    } catch (e: any) {
      vite?.ssrFixStacktrace(e)
      next(e)
    }
  })

  return { app }
}

createServer().then(({ app }) => {
  const port = process.env.PORT || 3000
  app.listen(port, () => {
    console.log(`SSR Server running on http://localhost:${port}`)
  })
})
