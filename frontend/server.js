import http from 'node:http'
import fs from 'node:fs/promises'
import express from 'express'
import { createServer as createViteServer } from 'vite'
import { createClient } from 'redis'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const isProduction = process.env.NODE_ENV === 'production'
const port = process.env.PORT || 5173
const base = process.env.BASE || '/'

const apiHost = process.env.API_HOST || '127.0.0.1'
const apiPort = process.env.API_PORT || '8000'

const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379'
})

redisClient.on('error', () => {})

redisClient.connect().then(() => {
  console.log('  \x1b[32m➜\x1b[0m  \x1b[32m[Redis/Valkey]\x1b[0m Connected and caching enabled');
}).catch(() => {
  console.log('  \x1b[33m➜\x1b[0m  \x1b[33m[Redis/Valkey]\x1b[0m Not connected (caching disabled)');
})

async function createServer() {
  const app = express()

  app.use('/api', (req, res, next) => {
    const options = {
      hostname: apiHost,
      port: parseInt(apiPort),
      path: req.originalUrl,
      method: req.method,
      headers: { ...req.headers, host: `${apiHost}:${apiPort}` }
    };
    const proxyReq = http.request(options, (proxyRes) => {
      res.writeHead(proxyRes.statusCode || 500, proxyRes.headers);
      proxyRes.pipe(res, { end: true });
    });
    req.pipe(proxyReq, { end: true });
    proxyReq.on('error', (err) => {
      console.error('[Proxy Error]:', err.message);
      res.status(500).end();
    });
  })


  let vite
  if (!isProduction) {
    vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'custom',
      base
    })
    app.use(vite.middlewares)
  } else {
    const compression = (await import('compression')).default
    const sirv = (await import('sirv')).default
    app.use(compression())
    app.use(base, sirv(path.resolve(__dirname, 'dist/client'), { 
      extensions: [], 
      gzip: true,
      index: false 
    }))
  }

  app.use(async (req, res) => {
    try {
      const url = req.originalUrl.replace(base, '') || '/'    

      if (url !== '/' && url.includes('.')) {
        return res.status(404).end()
      }

      if (redisClient.isReady && isProduction) {
        const cachedHtml = await redisClient.get(`ssr:${url}`)
        if (cachedHtml) {
          return res.status(200).set({ 'Content-Type': 'text/html' }).end(cachedHtml)
        }
      }

      let template
      let render

      if (!isProduction) {
        template = await fs.readFile(path.resolve(__dirname, 'index.html'), 'utf-8')
        template = await vite.transformIndexHtml(url, template)
        render = (await vite.ssrLoadModule('/src/entry-server.ts')).render
      } else {
        template = await fs.readFile(path.resolve(__dirname, 'dist/client/index.html'), 'utf-8')
        render = (await import('./dist/server/entry-server.js')).render
      }

      const { html, state } = await render(url)
      
      const stateHtml = `<script>window.__INITIAL_STATE__=${JSON.stringify(state)}</script>`
      
      const finalHtml = template
        .replace('<div id="app"></div>', `<div id="app">${html}</div>`)
        .replace('</body>', `${stateHtml}</body>`)

      if (redisClient.isReady && isProduction) {
        await redisClient.setEx(`ssr:${url}`, 3600, finalHtml)
      }

      res.status(200).set({ 'Content-Type': 'text/html' }).end(finalHtml)
    } catch (e) {
      if (!isProduction) {
        vite.ssrFixStacktrace(e)
      }
      console.error(`[SSR Error]: ${e.stack}`)
      res.status(500).end(e.stack)
    }
  })

  return { app }
}

createServer().then(({ app }) => {
  app.listen(port, () => {
    console.log(`\n  \x1b[32m➜\x1b[0m  \x1b[1mLocal:\x1b[0m   \x1b[36mhttp://localhost:${port}/\x1b[0m`)
    console.log(`  \x1b[32m➜\x1b[0m  \x1b[1mMode:\x1b[0m    \x1b[33m${isProduction ? 'Production' : 'Development'} (SSR)\x1b[0m`)
  })
})
