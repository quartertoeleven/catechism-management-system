<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar :title="t('menu.grade.unitList')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>

      <UDashboardToolbar />
    </template>

    <template #body>
      <p>Unit List — coming soon.</p>
    </template>
  </UDashboardPanel>
</template>
