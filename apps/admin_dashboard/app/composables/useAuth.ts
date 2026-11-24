interface SessionUser {
  subject: string
  name: string | null
  email: string | null
  picture: string | null
}

interface SessionCatechist {
  id: string
  code: string
  full_name: string
}

interface SessionResponse {
  authenticated: boolean
  user: SessionUser | null
  catechist: SessionCatechist | null
}

const SESSION_PATH = '/auth/session'
const LOGIN_PATH = '/auth/login'
const LOGOUT_PATH = '/auth/logout'
const DEFAULT_RETURN_TO = '/'

const ANONYMOUS_SESSION: SessionResponse = {
  authenticated: false,
  user: null,
  catechist: null
}

export function useAuth() {
  const session = useState<SessionResponse>('auth-session', () => ANONYMOUS_SESSION)
  const loaded = useState<boolean>('auth-session-loaded', () => false)

  async function fetchSession(force = false): Promise<SessionResponse> {
    if (loaded.value && !force) {
      return session.value
    }

    try {
      session.value = await $fetch<SessionResponse>(SESSION_PATH, {
        credentials: 'include'
      })
    } catch {
      session.value = ANONYMOUS_SESSION
    }

    loaded.value = true
    return session.value
  }

  function resetSession(): void {
    session.value = ANONYMOUS_SESSION
    loaded.value = false
  }

  function signIn(returnTo: string = DEFAULT_RETURN_TO): void {
    if (!import.meta.client) {
      return
    }

    const query = new URLSearchParams({ return_to: returnTo })
    window.location.assign(`${LOGIN_PATH}?${query.toString()}`)
  }

  function signOut(): void {
    if (!import.meta.client) {
      return
    }

    window.location.assign(LOGOUT_PATH)
  }

  return {
    session,
    user: computed(() => session.value.user),
    catechist: computed(() => session.value.catechist),
    isAuthenticated: computed(() => session.value.authenticated),
    fetchSession,
    signIn,
    signOut,
    resetSession
  }
}
