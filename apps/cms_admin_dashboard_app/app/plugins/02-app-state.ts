import { getAppState as fetchAppState } from '~/generated-client'

export default defineNuxtPlugin(async () => {
  const { checkAuth } = useAuth()

  const user = await checkAuth()
  if (!user) {
    return
  }

  try {
    const result = await fetchAppState({})
    Object.entries(result).forEach(([key, value]) => {
      setAppStateIfAbsent(key, value)
    })
  } catch {
    // App load must not break; 401 is handled by the 01-api-client interceptor.
  }
})
