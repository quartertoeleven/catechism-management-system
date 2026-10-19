export function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

export function randomFrom<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)]!
}

/** `RRGGBB` / `#RRGGBB` -> CSS-ready `#RRGGBB` (bare hex is invalid in `style` bindings) */
export function toCssColor(color: string | null | undefined, fallback = '#6b7280'): string {
  if (!color) return fallback
  return color.startsWith('#') ? color : `#${color}`
}
