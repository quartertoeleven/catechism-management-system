<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { upperFirst } from 'scule'
import { getPaginationRowModel } from '@tanstack/table-core'
import { listScheduleActivityTypes, type ScheduleActivityTypeListItem } from '~/generated-client'

enum FetchStatus {
  Pending = 'pending',
  Success = 'success',
  Error = 'error'
}

const { t } = useI18n()
const table = useTemplateRef('table')

const data = ref<ScheduleActivityTypeListItem[]>([])
const status = ref<FetchStatus>(FetchStatus.Pending)
const columnVisibility = ref()

const UBadge = resolveComponent('UBadge')
const UButton = resolveComponent('UButton')

onMounted(async () => {
  try {
    const result = await listScheduleActivityTypes({})
    data.value = result.data ?? []
    status.value = FetchStatus.Success
  } catch {
    status.value = FetchStatus.Error
  }
})

const search = computed({
  get: (): string => {
    return (table.value?.tableApi?.getColumn('name')?.getFilterValue() as string) || ''
  },
  set: (value: string) => {
    table.value?.tableApi?.getColumn('name')?.setFilterValue(value || undefined)
  }
})

const columnLabels: Record<string, string> = {
  code: t('listManagement.scheduleActivityType.code'),
  name: t('listManagement.scheduleActivityType.name'),
  color: t('listManagement.scheduleActivityType.color'),
  is_system: t('listManagement.scheduleActivityType.isSystem')
}

const columns: TableColumn<ScheduleActivityTypeListItem>[] = [
  {
    accessorKey: 'code',
    header: () => h(UButton, {
      color: 'neutral',
      variant: 'ghost',
      label: t('listManagement.scheduleActivityType.code')
    })
  },
  {
    accessorKey: 'name',
    header: () => h(UButton, {
      color: 'neutral',
      variant: 'ghost',
      label: t('listManagement.scheduleActivityType.name')
    })
  },
  {
    accessorKey: 'color',
    header: t('listManagement.scheduleActivityType.color'),
    cell: ({ row }) => {
      const color = row.original.color
      if (!color) return h('span', { class: 'text-muted' }, '—')
      return h('div', { class: 'flex items-center gap-2' }, [
        h('span', {
          class: 'inline-block w-3 h-3 rounded-full shrink-0',
          style: { backgroundColor: `#${color}` }
        }),
        h('span', { class: 'text-muted text-xs' }, `#${color}`)
      ])
    }
  },
  {
    accessorKey: 'is_system',
    header: t('listManagement.scheduleActivityType.isSystem'),
    cell: ({ row }) => h(UBadge, {
      color: row.original.is_system ? 'success' : 'neutral',
      variant: 'subtle'
    }, () => row.original.is_system ? t('common.yes') : t('common.no'))
  }
]

const pagination = ref({
  pageIndex: 0,
  pageSize: 10
})
</script>

<template>
  <UDashboardPanel id="schedule-activity-types">
    <template #header>
      <UDashboardNavbar :title="t('listManagement.scheduleActivityTypes')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            :label="t('listManagement.addScheduleActivityType')"
            icon="i-lucide-plus"
          />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div class="flex flex-wrap items-center justify-between gap-1.5">
        <UInput
          v-model="search"
          class="max-w-sm"
          icon="i-lucide-search"
          :placeholder="t('listManagement.searchScheduleActivityTypes')"
        />

        <UDropdownMenu
          :items="
            table?.tableApi
              ?.getAllColumns()
              .filter((column: any) => column.getCanHide())
              .map((column: any) => ({
                label: columnLabels[column.id] || upperFirst(column.id),
                type: 'checkbox' as const,
                checked: column.getIsVisible(),
                onUpdateChecked(checked: boolean) {
                  table?.tableApi?.getColumn(column.id)?.toggleVisibility(!!checked)
                },
                onSelect(e?: Event) {
                  e?.preventDefault()
                }
              }))
          "
          :content="{ align: 'end' }"
        >
          <UButton
            :label="t('listManagement.display')"
            color="neutral"
            variant="outline"
            trailing-icon="i-lucide-settings-2"
          />
        </UDropdownMenu>
      </div>

      <UTable
        ref="table"
        v-model:column-visibility="columnVisibility"
        v-model:pagination="pagination"
        :pagination-options="{
          getPaginationRowModel: getPaginationRowModel()
        }"
        class="shrink-0"
        :data="data"
        :columns="columns"
        :loading="status === FetchStatus.Pending"
        :ui="{
          base: 'table-fixed border-separate border-spacing-0',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-2 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r',
          td: 'border-b border-default',
          separator: 'h-0'
        }"
      >
        <template #loading>
          <div class="flex justify-center py-6">
            <UEmpty
              loading
              icon="i-lucide-list"
              class="text-primary"
              :title="t('listManagement.loadingScheduleActivityTypes')"
            />
          </div>
        </template>

        <template #empty>
          <div class="flex justify-center py-6">
            <UEmpty
              icon="i-lucide-list"
              :title="t('listManagement.emptyScheduleActivityTypes.title')"
              :description="t('listManagement.emptyScheduleActivityTypes.description')"
              :actions="[{
                icon: 'i-lucide-plus',
                label: t('listManagement.addScheduleActivityType')
              }]"
            />
          </div>
        </template>
      </UTable>

      <div v-if="status === FetchStatus.Pending || data.length > 0" class="flex items-center justify-between gap-3 border-t border-default pt-4 mt-auto">
        <div class="text-sm text-muted">
          {{ table?.tableApi?.getFilteredRowModel().rows.length || 0 }} row(s)
        </div>

        <div class="flex items-center gap-1.5">
          <UPagination
            :default-page="(table?.tableApi?.getState().pagination.pageIndex || 0) + 1"
            :items-per-page="table?.tableApi?.getState().pagination.pageSize"
            :total="table?.tableApi?.getFilteredRowModel().rows.length"
            @update:page="(p: number) => table?.tableApi?.setPageIndex(p - 1)"
          />
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
