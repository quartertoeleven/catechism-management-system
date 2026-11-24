const LOGIN_PATH = '/login'
const DEFAULT_RETURN_TO = '/'
const RETURN_TO_QUERY = 'return_to'

export default defineNuxtRouteMiddleware(async (to) => {
  // The BFF reads cookies from the browser; the server render has no session.
  if (import.meta.server) {
    return
  }

  const { fetchSession, isAuthenticated } = useAuth()
  await fetchSession()

  if (!isAuthenticated.value && to.path !== LOGIN_PATH) {
    return navigateTo({
      path: LOGIN_PATH,
      query: { [RETURN_TO_QUERY]: to.fullPath }
    })
  }

  if (isAuthenticated.value && to.path === LOGIN_PATH) {
    return navigateTo(safeReturnTo(to.query[RETURN_TO_QUERY] ?? DEFAULT_RETURN_TO))
  }
})
