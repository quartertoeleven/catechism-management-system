// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['@nuxt/eslint', '@nuxt/ui', '@vueuse/nuxt', '@nuxtjs/i18n'],
  compatibilityDate: '2026-06-30',

  ssr: false,

  devtools: {
    enabled: true
  },
  css: ['~/assets/scss/custom.scss', '~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: ''
    }
  },
  i18n: {
    strategy: 'no_prefix',
    defaultLocale: 'vi',
    locales: [
      { code: 'vi', language: 'vi-VN', file: 'vi.json' }
    ],
  },
  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})