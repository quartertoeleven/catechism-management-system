<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const toast = useToast()
const { signIn } = useAuth()

const CATECHIST_NOT_LINKED = 'catechist_not_linked'
const KNOWN_ERRORS = ['invalid_flow', 'missing_code', 'authentication_failed']

// Served from `public/`, so it stays a runtime URL instead of a bundler import.
const loginBackground = '/images/login-bg.jpg'

const returnTo = computed(() => safeReturnTo(route.query.return_to))

const errorMessage = computed(() => {
  const error = route.query.error
  if (typeof error !== 'string' || !error || error === CATECHIST_NOT_LINKED) {
    return undefined
  }
  const key = KNOWN_ERRORS.includes(error) ? error : 'unknown'
  return t(`auth.errors.${key}`)
})

onMounted(() => {
  if (route.query.error !== CATECHIST_NOT_LINKED) {
    return
  }

  toast.add({
    title: t('auth.errors.catechist_not_linked.title'),
    description: t('auth.errors.catechist_not_linked.description'),
    color: 'error',
    icon: 'i-lucide-circle-alert'
  })

  const query = { ...route.query }
  delete query.error
  router.replace({ query })
})

useSeoMeta({
  title: () => t('login.title')
})

useHead({
  htmlAttrs: {
    lang: 'vi'
  }
})

function onLoginButtonClick() {
  signIn(returnTo.value)
}
</script>

<template>
  <div class="flex min-h-svh bg-default lg:h-svh">
    <!-- Illustration placeholder: replace /images/login-bg.jpg with the final image -->
    <div class="relative hidden w-1/2 overflow-hidden bg-muted lg:block">
      <img
        :src="loginBackground"
        alt=""
        class="absolute inset-0 size-full scale-105 object-cover"
      >
      <div class="absolute inset-0 bg-gradient-to-br from-black/25 via-transparent to-black/30" />
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_60%,rgba(0,0,0,0.25))]" />
      <div class="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/30 to-transparent" />
    </div>

    <div class="flex w-full flex-col px-4 py-12 lg:w-1/2">
      <div class="flex flex-1 items-center justify-center">
        <div class="w-full max-w-md text-center">
          <div
            class="mx-auto mb-6 flex size-16 items-center justify-center rounded-2xl bg-primary/10 ring-1 ring-primary/20"
          >
            <UIcon name="i-lucide-graduation-cap" class="size-8 text-primary" />
          </div>

          <h1 class="text-2xl font-bold tracking-tight text-highlighted">
            {{ t('login.title') }}
          </h1>

          <p class="mt-2 text-muted">
            {{ t('login.subheader.line1') }}<br>{{ t('login.subheader.line2') }}
          </p>

          <UAlert
            v-if="errorMessage"
            :title="errorMessage"
            color="error"
            variant="subtle"
            icon="i-lucide-circle-alert"
            class="mt-6 text-left"
          />

          <UButton
            :label="t('login.signIn')"
            icon="i-lucide-log-in"
            block
            size="lg"
            class="mt-8"
            @click="onLoginButtonClick"
          />
        </div>
      </div>

      <footer class="text-center text-sm text-dimmed">
        {{ t('login.footer.developedBy') }}
        <strong>{{ t('login.footer.organization') }}</strong><br>
        {{ t('login.footer.copyright') }}
        <strong>{{ t('login.footer.organization') }}</strong>
        - {{ t('login.footer.releasedUnder') }}
        <NuxtLink
          to="https://github.com/quartertoeleven/catechism-management-system"
          target="_blank"
          class="text-primary underline"
        >
          {{ t('login.footer.license') }}
        </NuxtLink>
      </footer>
    </div>
  </div>
</template>
