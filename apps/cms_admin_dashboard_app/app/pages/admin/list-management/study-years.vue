<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { upperFirst } from 'scule'
import { getPaginationRowModel } from '@tanstack/table-core'
import type { Row } from '@tanstack/table-core'
import { listStudyYears, type StudyYearListItem } from '~/generated-client'

enum FetchStatus {
  Pending = 'pending',
  Success = 'success',
  Error = 'error'
}

const { t } = useI18n()
const table = useTemplateRef('table')

const data = ref<StudyYearListItem[]>([])
const status = ref<FetchStatus>(FetchStatus.Pending)
const columnVisibility = ref()

const UBadge = resolveComponent('UBadge')
const UButton = resolveComponent('UButton')
const UDropdownMenu = resolveComponent('UDropdownMenu')

onMounted(async () => {
  try {
    const result = await listStudyYears({})
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

function getRowItems(row: Row<StudyYearListItem>) {
  return [
    {
      label: t('listManagement.studyYear.setCurrent'),
      icon: 'i-lucide-check-circle',
      onSelect() {
        alert('Set as current — coming soon')
      }
    },
    {
      label: row.original.is_readonly
        ? t('listManagement.studyYear.setWritable')
        : t('listManagement.studyYear.setReadOnly'),
      icon: row.original.is_readonly ? 'i-lucide-lock-open' : 'i-lucide-lock',
      onSelect() {
        alert('Toggle read-only — coming soon')
      }
    }
  ]
}

const columnLabels: Record<string, string> = {
  code: t('listManagement.studyYear.code'),
  name: t('listManagement.studyYear.name'),
  is_current: t('listManagement.studyYear.isCurrent'),
  is_readonly: t('listManagement.studyYear.isReadonly')
}

const columns: TableColumn<StudyYearListItem>[] = [
  {
    accessorKey: 'code',
    header: () => h(UButton, {
      color: 'neutral',
      variant: 'ghost',
      label: t('listManagement.studyYear.code')
    })
  },
  {
    accessorKey: 'name',
    header: () => h(UButton, {
      color: 'neutral',
      variant: 'ghost',
      label: t('listManagement.studyYear.name')
    })
  },
  {
    accessorKey: 'is_current',
    header: t('listManagement.studyYear.isCurrent'),
    cell: ({ row }) => h(UBadge, {
      color: row.original.is_current ? 'success' : 'neutral',
      variant: 'subtle'
    }, () => row.original.is_current ? t('common.yes') : t('common.no'))
  },
  {
    accessorKey: 'is_readonly',
    header: t('listManagement.studyYear.isReadonly'),
    cell: ({ row }) => h(UBadge, {
      color: row.original.is_readonly ? 'warning' : 'neutral',
      variant: 'subtle'
    }, () => row.original.is_readonly ? t('common.yes') : t('common.no'))
  },
  {
    id: 'actions',
    enableHiding: false,
    cell: ({ row }) => h(
      'div',
      { class: 'text-right' },
      h(
        UDropdownMenu,
        { content: { align: 'end' }, items: getRowItems(row) },
        () => h(UButton, {
          icon: 'i-lucide-ellipsis-vertical',
          color: 'neutral',
          variant: 'ghost',
          class: 'ml-auto'
        })
      )
    )
  }
]

const pagination = ref({
  pageIndex: 0,
  pageSize: 10
})
</script>

<template>
  <UDashboardPanel id="study-years">
    <template #header>
      <UDashboardNavbar :title="t('listManagement.studyYears')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UButton
            :label="t('listManagement.addStudyYear')"
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
          :placeholder="t('listManagement.searchStudyYears')"
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
              icon="i-lucide-calendar"
              class="text-primary"
              :title="t('listManagement.loadingStudyYears')"
            />
          </div>
        </template>

        <template #empty>
          <div class="flex justify-center py-6">
            <UEmpty
              icon="i-lucide-calendar"
              :title="t('listManagement.emptyStudyYears.title')"
              :description="t('listManagement.emptyStudyYears.description')"
              :actions="[{
                icon: 'i-lucide-plus',
                label: t('listManagement.addStudyYear')
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
