export interface CurrentUser {
  sub: string
  name?: string
  username?: string
  email?: string
  picture?: string
}

const user = ref<CurrentUser | null>(null)
const pending = ref(false)
const checked = ref(false)
let checkAuthPromise: Promise<CurrentUser | null> | null = null

export function useAuth() {
  function checkAuth(): Promise<CurrentUser | null> {
    if (checked.value) {
      return Promise.resolve(user.value)
    }
    if (checkAuthPromise) {
      return checkAuthPromise
    }
    checkAuthPromise = (async () => {
      pending.value = true
      try {
        user.value = await $fetch<CurrentUser>(
          `${getApiBase()}/dashboard-api/auth/me`,
          { credentials: 'include' }
        )
      } catch {
        user.value = null
      } finally {
        pending.value = false
        checked.value = true
        checkAuthPromise = null
      }
      return user.value
    })()
    return checkAuthPromise
  }

  return { user, pending, checkAuth }
}
