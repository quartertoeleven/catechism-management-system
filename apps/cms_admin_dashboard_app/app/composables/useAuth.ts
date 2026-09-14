import { myProfile, type UserProfileResponse } from '~/generated-client'

const user = ref<UserProfileResponse | null>(null)
const pending = ref(false)
const checked = ref(false)
let checkAuthPromise: Promise<UserProfileResponse | null> | null = null

export function useAuth() {
  function checkAuth(): Promise<UserProfileResponse | null> {
    if (checked.value) {
      return Promise.resolve(user.value)
    }
    if (checkAuthPromise) {
      return checkAuthPromise
    }
    checkAuthPromise = (async () => {
      pending.value = true
      try {
        const result = await myProfile({})
        user.value = result
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

  function resetAuth() {
    user.value = null
    checked.value = false
    checkAuthPromise = null
  }

  return { user, pending, checkAuth, resetAuth }
}
