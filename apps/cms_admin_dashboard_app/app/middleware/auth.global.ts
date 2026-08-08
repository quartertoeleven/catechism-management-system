export default defineNuxtRouteMiddleware(async (to) => {
  const { checkAuth } = useAuth()
  const user = await checkAuth()

  if (to.path === '/login') {
    if (user) {
      return navigateTo('/')
    }
  } else if (!user) {
    return navigateTo('/login')
  }
})
