export const APP_STATE_KEY_PREFIX = 'app_state_'

export function setAppState(key: string, value: unknown): void {
  localStorage.setItem(`${APP_STATE_KEY_PREFIX}${key}`, JSON.stringify(value))
}

export function setAppStateIfAbsent(key: string, value: unknown): void {
  const storageKey = `${APP_STATE_KEY_PREFIX}${key}`
  if (localStorage.getItem(storageKey) !== null) {
    return
  }
  localStorage.setItem(storageKey, JSON.stringify(value))
}

export function getAppState<T>(key: string): T | null {
  try {
    const raw = localStorage.getItem(`${APP_STATE_KEY_PREFIX}${key}`)
    return raw === null ? null : (JSON.parse(raw) as T)
  } catch {
    return null
  }
}
