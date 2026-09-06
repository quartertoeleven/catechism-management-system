<script setup lang="ts">
const { t } = useI18n()
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar :title="t('menu.class.examScores')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>
      </UDashboardNavbar>

      <UDashboardToolbar />
    </template>

    <template #body>
      <p>Class Exam Scores — coming soon.</p>
    </template>
  </UDashboardPanel>
</template>
