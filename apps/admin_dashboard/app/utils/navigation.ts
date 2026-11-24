const DEFAULT_RETURN_TO = '/'
const LOCAL_PATH_PREFIX = '/'
const PROTOCOL_RELATIVE_PREFIX = '//'

export function safeReturnTo(value: unknown): string {
  if (typeof value !== 'string') {
    return DEFAULT_RETURN_TO
  }
  if (!value.startsWith(LOCAL_PATH_PREFIX) || value.startsWith(PROTOCOL_RELATIVE_PREFIX)) {
    return DEFAULT_RETURN_TO
  }
  return value
}
