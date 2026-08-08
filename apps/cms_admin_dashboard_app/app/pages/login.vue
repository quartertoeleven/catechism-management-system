<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const loginUrl = `${getApiBase()}/dashboard-api/auth/login`
</script>

<template>
  <div class="flex min-h-svh lg:h-svh">
    <div class="relative hidden w-1/2 overflow-hidden bg-neutral-100 lg:block">
      <img
        src="/images/login-bg.jpg"
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

          <h1 class="text-2xl font-bold tracking-tight">
            Trang quản trị
          </h1>

          <p class="mt-2 text-md text-dimmed">
            Hệ thống Quản Lý Giáo Lý<br>Thiếu Nhi Tam Hà
          </p>

          <UButton
            :to="loginUrl"
            label="Đăng nhập"
            icon="i-lucide-log-in"
            block
            size="lg"
            class="mt-8"
          />
        </div>
      </div>

      <footer class="text-center text-sm text-dimmed">
        Phát triển bởi <strong>Quarter To Eleven</strong><br>
        Bản quyền 2026 bởi <strong>Quarter To Eleven</strong> - Phát hành dưới
        <NuxtLink
          to="https://github.com/quartertoeleven/catechism-management-system"
          target="_blank"
          class="text-primary underline"
        >
          Giấy Phép MIT
        </NuxtLink>
      </footer>
    </div>
  </div>
</template>
