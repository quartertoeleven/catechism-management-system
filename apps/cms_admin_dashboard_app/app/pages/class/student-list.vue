<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar :title="t('menu.class.studentList')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>

      <UDashboardToolbar />
    </template>

    <template #body>
      <p>Student List — coming soon.</p>
    </template>
  </UDashboardPanel>
</template>
