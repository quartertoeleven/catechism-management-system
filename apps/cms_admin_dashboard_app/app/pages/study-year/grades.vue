<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import {
  listGrades,
  type GradeListItem,
  type StudyYearInfo
} from '~/generated-client'

const { t } = useI18n()

const grades = ref<GradeListItem[]>([])
const loadStatus = ref<'pending' | 'success' | 'error'>('pending')

const UButton = resolveComponent('UButton')

async function loadGrades() {
  loadStatus.value = 'pending'
  try {
    const stored = getAppState<StudyYearInfo>('current_selected_study_year')
    const result = stored?.code
      ? await listGrades({ query: { study_year_code: stored.code } })
      : await listGrades({})
    grades.value = result.data ?? []
    loadStatus.value = 'success'
  } catch {
    loadStatus.value = 'error'
  }
}

onMounted(loadGrades)

const addOpen = ref(false)
const editGradeId = ref<string | null>(null)

// Clear the stale id on close so the dialog's internal trigger
// (navbar / empty-state button) always opens in create mode.
watch(addOpen, (isOpen) => {
  if (!isOpen) editGradeId.value = null
})

function openAddDialog() {
  addOpen.value = true
}

function onEditGrade(grade: GradeListItem) {
  editGradeId.value = grade.id
  addOpen.value = true
}

function onCreateGrade(grade: GradeListItem) {
  const next = [...grades.value, grade]
  next.sort((a, b) => a.code.localeCompare(b.code))
  grades.value = next
}

function onUpdateGrade(grade: GradeListItem) {
  grades.value = grades.value.map(existing =>
    existing.id === grade.id ? grade : existing
  )
}

const deleteOpen = ref(false)
const deleteTarget = ref<GradeListItem | null>(null)

function onDeleteClick(grade: GradeListItem) {
  deleteTarget.value = grade
  deleteOpen.value = true
}

function onDeleteGrade(gradeId: string) {
  grades.value = grades.value.filter(existing => existing.id !== gradeId)
}

const columns: TableColumn<GradeListItem>[] = [
  {
    accessorKey: 'code',
    header: () => h(UButton, {
      color: 'neutral',
      variant: 'ghost',
      label: t('studyYearGrades.columns.code'),
      class: '-mx-2.5'
    }),
    meta: {
      class: {
        th: 'w-[calc(50%-3.5rem)]',
        td: 'w-[calc(50%-3.5rem)]'
      }
    }
  },
  {
    accessorKey: 'name',
    header: () => h(UButton, {
      color: 'neutral',
      variant: 'ghost',
      label: t('studyYearGrades.columns.name'),
      class: '-mx-2.5'
    }),
    meta: {
      class: {
        th: 'w-[calc(50%-3.5rem)]',
        td: 'w-[calc(50%-3.5rem)]'
      }
    }
  },
  {
    id: 'actions',
    header: '',
    enableHiding: false,
    meta: {
      class: {
        th: 'w-28',
        td: 'w-28'
      }
    }
  }
]
</script>

<template>
  <UDashboardPanel>
    <template #header>
      <UDashboardNavbar :title="t('menu.studyYear.grades')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <GradeAddDialog
            v-model:open="addOpen"
            :grade-id="editGradeId"
            @create="onCreateGrade"
            @update="onUpdateGrade"
          />
          <GradeDeleteDialog
            v-model:open="deleteOpen"
            :grade="deleteTarget"
            @delete="onDeleteGrade"
          />
        </template>
      </UDashboardNavbar>
    </template>

    <template #body>
      <div
        v-if="loadStatus === 'error'"
        class="flex items-center gap-2 text-sm text-error"
      >
        <span>{{ t('studyYearGrades.loadError') }}</span>
        <UButton
          :label="t('studyYearGrades.retry')"
          color="error"
          variant="soft"
          size="xs"
          @click="loadGrades"
        />
      </div>

      <div
        v-if="loadStatus === 'pending'"
        class="space-y-2"
        aria-busy="true"
        role="status"
      >
        <!-- Same columns as the table: Mã khối | Tên khối | actions -->
        <div
          v-for="n in 5"
          :key="n"
          class="flex items-center gap-4"
        >
          <USkeleton class="h-12 grow basis-0" />
          <USkeleton class="h-12 grow basis-0" />
          <USkeleton class="h-12 w-28 shrink-0" />
        </div>
      </div>

      <UTable
        v-if="loadStatus === 'success'"
        :data="grades"
        :columns="columns"
        class="shrink-0"
        :ui="{
          base: 'table-fixed border-separate border-spacing-0',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-2 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r',
          td: 'border-b border-default',
          separator: 'h-0'
        }"
      >
        <template #empty>
          <div class="flex justify-center py-6">
            <UEmpty
              icon="i-lucide-layers"
              :title="t('studyYearGrades.empty.title')"
              :description="t('studyYearGrades.empty.description')"
              :actions="[{
                icon: 'i-lucide-plus',
                label: t('studyYearGrades.addGrade'),
                onClick: openAddDialog
              }]"
            />
          </div>
        </template>

        <template #actions-cell="{ row }">
          <div class="flex items-center justify-end gap-1">
            <UTooltip :text="t('studyYearGrades.actions.edit')">
              <UButton
                icon="i-lucide-pencil"
                color="neutral"
                variant="ghost"
                size="xs"
                :aria-label="t('studyYearGrades.actions.edit')"
                @click="onEditGrade(row.original)"
              />
            </UTooltip>
            <UTooltip :text="t('studyYearGrades.actions.delete')">
              <UButton
                icon="i-lucide-trash-2"
                color="error"
                variant="ghost"
                size="xs"
                :aria-label="t('studyYearGrades.actions.delete')"
                @click="onDeleteClick(row.original)"
              />
            </UTooltip>
          </div>
        </template>
      </UTable>
    </template>
  </UDashboardPanel>
</template>
