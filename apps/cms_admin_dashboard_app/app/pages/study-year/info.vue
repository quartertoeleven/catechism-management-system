<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar :title="t('menu.studyYear.info')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>

      <UDashboardToolbar />
    </template>

    <template #body>
      <p>Study Year Info — coming soon.</p>
    </template>
  </UDashboardPanel>
</template>
