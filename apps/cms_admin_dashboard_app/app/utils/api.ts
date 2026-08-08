export function getApiBase(): string {
  const config = useRuntimeConfig()
  return config.public.apiBase || 'http://localhost:8000'
}
