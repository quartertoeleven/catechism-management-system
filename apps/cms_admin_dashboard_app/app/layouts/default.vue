<script setup lang="ts">
import type { NavigationMenuItem } from '@nuxt/ui'

const route = useRoute()
const toast = useToast()
const { t } = useI18n()

const open = ref(false)

const links = {
  studyYear: [{
    label: t('menu.studyYear.label'),
    type: 'label',
    class: 'text-muted'
  }, {
    label: t('menu.studyYear.info'),
    icon: 'i-lucide-info',
    to: '/study-year/info',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.studyYear.schedules'),
    icon: 'i-lucide-calendar-days',
    to: '/study-year/schedules',
    onSelect: () => {
      open.value = false
    }
  }],
  grade: [{
    label: t('menu.grade.label'),
    type: 'label',
    class: 'text-muted'
  }, {
    label: t('menu.grade.dashboard'),
    icon: 'i-lucide-layout-dashboard',
    to: '/grade/dashboard',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.grade.unitList'),
    icon: 'i-lucide-group',
    to: '/grade/unit-list',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.grade.schedules'),
    icon: 'i-lucide-calendar-days',
    to: '/grade/schedules',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.grade.exams'),
    icon: 'i-lucide-book-open-check',
    to: '/grade/exams',
    onSelect: () => {
      open.value = false
    }
  }],
  class: [{
    label: t('menu.class.label'),
    type: 'label',
    class: 'text-muted'
  }, {
    label: t('menu.class.dashboard'),
    icon: 'i-lucide-layout-dashboard',
    to: '/class/dashboard',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.class.studentList'),
    icon: 'i-lucide-users',
    to: '/class/student-list',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.class.attendances'),
    icon: 'i-lucide-list-checks',
    to: '/class/attendances',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.class.examScores'),
    icon: 'i-lucide-file-check',
    to: '/class/exam-scores',
    onSelect: () => {
      open.value = false
    }
  }],
  adminArea: [{
    label: t('menu.adminArea.label'),
    type: 'label',
    class: 'text-muted'
  }, {
    label: t('menu.adminArea.listsManagement'),
    icon: 'i-lucide-list',
    defaultOpen: true,
    type: 'trigger',
    children: [{
      label: t('listManagement.studyYears'),
      to: '/admin/list-management/study-years',
      onSelect: () => {
        open.value = false
      }
    }, {
      label: t('listManagement.scheduleActivityTypes'),
      to: '/admin/list-management/schedule-activity-type',
      onSelect: () => {
        open.value = false
      }
    }]
  }],
  willBeRemoved: [{
    label: t('menu.willBeRemoved.label'),
    type: 'label',
    class: 'text-muted'
  }, {
    label: t('menu.willBeRemoved.home'),
    icon: 'i-lucide-house',
    to: '/',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.willBeRemoved.inbox'),
    icon: 'i-lucide-inbox',
    to: '/inbox',
    badge: '4',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.willBeRemoved.customers'),
    icon: 'i-lucide-users',
    to: '/customers',
    onSelect: () => {
      open.value = false
    }
  }, {
    label: t('menu.willBeRemoved.settings.label'),
    to: '/settings',
    icon: 'i-lucide-settings',
    defaultOpen: true,
    type: 'trigger',
    children: [{
      label: t('menu.willBeRemoved.settings.general'),
      to: '/settings',
      exact: true,
      onSelect: () => {
        open.value = false
      }
    }, {
      label: t('menu.willBeRemoved.settings.members'),
      to: '/settings/members',
      onSelect: () => {
        open.value = false
      }
    }, {
      label: t('menu.willBeRemoved.settings.notifications'),
      to: '/settings/notifications',
      onSelect: () => {
        open.value = false
      }
    }, {
      label: t('menu.willBeRemoved.settings.security'),
      to: '/settings/security',
      onSelect: () => {
        open.value = false
      }
    }]
  }, {
    label: t('menu.willBeRemoved.feedback'),
    icon: 'i-lucide-message-circle',
    to: 'https://github.com/nuxt-ui-templates/dashboard',
    target: '_blank'
  }, {
    label: t('menu.willBeRemoved.helpAndSupport'),
    icon: 'i-lucide-info',
    to: 'https://github.com/nuxt-ui-templates/dashboard',
    target: '_blank'
  }]
} satisfies Record<string, NavigationMenuItem[]>

const groups = computed(() => [{
  id: 'links',
  label: t('search.goTo'),
  items: links
}, {
  id: 'code',
  label: t('search.code'),
  items: [{
    id: 'source',
    label: t('search.viewPageSource'),
    icon: 'i-simple-icons-github',
    to: `https://github.com/nuxt-ui-templates/dashboard/blob/main/app/pages${route.path === '/' ? '/index' : route.path}.vue`,
    target: '_blank'
  }]
}])

onMounted(async () => {
  const cookie = useCookie('cookie-consent')
  if (cookie.value === 'accepted') {
    return
  }

  toast.add({
    title: t('cookie.message'),
    duration: 0,
    close: false,
    actions: [{
      label: t('cookie.accept'),
      color: 'neutral',
      variant: 'outline',
      onClick: () => {
        cookie.value = 'accepted'
      }
    }, {
      label: t('cookie.optOut'),
      color: 'neutral',
      variant: 'ghost'
    }]
  })
})
</script>

<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar id="default" v-model:open="open" collapsible resizable class="bg-elevated/25"
      :ui="{ footer: 'lg:border-t lg:border-default', header: 'lg:border-b lg:border-default' }">
      <template #header="{ collapsed }">
        <TeamsMenu :collapsed="collapsed" />
      </template>

      <template #default="{ collapsed }">
        <UNavigationMenu :collapsed="collapsed" :items="links.studyYear" orientation="vertical" tooltip popover />

        <UNavigationMenu :collapsed="collapsed" :items="links.grade" orientation="vertical" tooltip />

        <UNavigationMenu :collapsed="collapsed" :items="links.class" orientation="vertical" tooltip />

        <UNavigationMenu :collapsed="collapsed" :items="links.adminArea" orientation="vertical" tooltip />

        <UNavigationMenu :collapsed="collapsed" :items="links.willBeRemoved" orientation="vertical" tooltip class="mt-auto" />
      </template>

      <template #footer="{ collapsed }">
        <UserMenu :collapsed="collapsed" />
      </template>
    </UDashboardSidebar>

    <!-- <UDashboardSearch :groups="groups" /> -->

    <slot />

    <NotificationsSlideover />
  </UDashboardGroup>
</template>
