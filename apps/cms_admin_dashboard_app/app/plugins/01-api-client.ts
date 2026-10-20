import { client } from '~/generated-client/client.gen'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const { resetAuth } = useAuth()

  client.setConfig({
    baseURL: config.public.apiBase,
    credentials: 'include',
    onResponse: async ({ response }) => {
      if (response.status === 401) {
        resetAuth()
        await navigateTo('/login')
      }
    }
  })
})
