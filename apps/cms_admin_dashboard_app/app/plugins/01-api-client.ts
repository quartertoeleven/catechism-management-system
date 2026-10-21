import { client } from '~/generated-client/client.gen'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const { resetAuth, isAuthCheckInProgress } = useAuth()

  client.setConfig({
    baseURL: config.public.apiBase,
    credentials: 'include',
    onResponse: async ({ response }) => {
      if (response.status === 401) {
        // While the auth check itself is in flight, it owns the redirect:
        // auth.global middleware handles the unauthenticated user afterward.
        if (isAuthCheckInProgress()) {
          return
        }

        resetAuth()
        await navigateTo('/login')
      }
    }
  })
})
