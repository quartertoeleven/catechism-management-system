/**
 * Dev-only proxy from the Nuxt origin to the FastAPI BFF.
 *
 * In production the edge reverse proxy routes `/auth/*` straight to the API,
 * so this route exists to keep the public URL contract identical locally.
 * `proxyRequest` forwards cookies and passes upstream 3xx responses through.
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const slug = getRouterParam(event, 'slug') ?? ''
  const { search } = getRequestURL(event)

  return proxyRequest(event, `${config.bffBaseUrl}/auth/${slug}${search}`, {
    fetchOptions: { redirect: 'manual' }
  })
})
