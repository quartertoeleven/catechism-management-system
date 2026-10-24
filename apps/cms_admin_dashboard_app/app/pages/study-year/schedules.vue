<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { getGroupedRowModel, type GroupingOptions } from '@tanstack/vue-table'
import { listGeneralSchedules, type GeneralScheduleListItem } from '~/generated-client'
import type { ScheduleActivity, ScheduleRow } from '~/types'

const { t } = useI18n()
const table = useTemplateRef('table')
const search = ref('')

const UButton = resolveComponent('UButton')

const expandToggle = ref(0)

function toggleExpandAll() {
  const allExpanded = table.value?.tableApi?.getIsAllRowsExpanded()
  table.value?.tableApi?.toggleAllRowsExpanded(!allExpanded)
  expandToggle.value++
}

const isAllExpanded = computed(() => {
  void expandToggle.value
  return table.value?.tableApi?.getIsAllRowsExpanded() ?? false
})

const expandLabel = computed(() => (isAllExpanded.value ? 'Thu gọn' : 'Mở rộng'))
const expandIcon = computed(() => (isAllExpanded.value ? 'i-lucide-chevrons-up' : 'i-lucide-chevrons-down'))

const filteredSchedules = computed(() => {
  if (!search.value.trim()) return schedules
  const q = search.value.toLowerCase()
  return schedules.filter(
    row =>
      row.date.includes(q)
      || row.activities.some(a => a.name.toLowerCase().includes(q))
  )
})

const monthNames = ['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8', 'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12']

function parseDate(dateStr: string) {
  const [day, month, year] = dateStr.split('-').map(Number)
  return { day, month, year }
}

function buildMonthKey(dateStr: string) {
  const { month, year } = parseDate(dateStr)
  return `${year}-${String(month).padStart(2, '0')}`
}

function formatMonthLabel(monthKey: string) {
  const [year, month] = monthKey.split('-').map(Number)
  return `${monthNames[month - 1]} - ${year}`
}

function parseDayName(dateStr: string) {
  const [dayStr, monthStr, yearStr] = dateStr.split('-')
  const formatted = new Intl.DateTimeFormat('vi-VN', { weekday: 'long' }).format(new Date(Number(yearStr), Number(monthStr) - 1, Number(dayStr)))
  // vi locale renders Sunday as "chủ nhật" — use the church terminology instead.
  if (formatted.toLowerCase() === 'chủ nhật') {
    return t('studyYearSchedules.dayNames.sunday')
  }
  // Title-case each word: "thứ hai" -> "Thứ Hai"
  return formatted
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

/** `yyyy-MM-dd` -> `dd-MM-yyyy` (row date format) */
function toRowDate(isoDate: string) {
  const [year, month, day] = isoDate.split('-')
  return `${day}-${month}-${year}`
}

/** `dd-MM-yyyy` -> `yyyy-MM-dd` (for date comparison) */
function toSortableDate(dateStr: string) {
  const [day, month, year] = dateStr.split('-')
  return `${year}-${month}-${day}`
}

function formatTime(isoDateTime: string) {
  return isoDateTime.slice(11, 16)
}

function formatDate(isoDateTime: string) {
  const [year, month, day] = isoDateTime.slice(0, 10).split('-')
  return `${day}/${month}/${year}`
}

function formatTimeRange(activity: ScheduleActivity) {
  if (!activity.endAt) {
    return t('studyYearSchedules.activityTime.from', { time: formatTime(activity.startAt) })
  }
  const sameDay = activity.startAt.slice(0, 10) === activity.endAt.slice(0, 10)
  if (sameDay) {
    return `${formatTime(activity.startAt)} - ${formatTime(activity.endAt)}`
  }
  return `${formatDate(activity.startAt)} ${formatTime(activity.startAt)} - ${formatDate(activity.endAt)} ${formatTime(activity.endAt)}`
}

const schedules = reactive<ScheduleRow[]>([])
const loadStatus = ref<'pending' | 'success' | 'error'>('pending')
const dialogOpen = ref(false)
const editingActivityId = ref<string | null>(null)
const duplicateMode = ref(false)
const deleteDialogOpen = ref(false)
const deletingActivity = ref<ScheduleActivity | null>(null)

function mapApiRows(items: GeneralScheduleListItem[]): ScheduleRow[] {
  const byDate = new Map<string, ScheduleActivity[]>()

  for (const item of items) {
    const isoDate = item.start_at.slice(0, 10)
    const activities = byDate.get(isoDate) ?? []
    activities.push({
      id: item.id,
      color: toCssColor(item.schedule_activity_type_color),
      activityTypeName: item.schedule_activity_type_name,
      name: item.name,
      startAt: item.start_at,
      endAt: item.end_at ?? undefined,
      isAttendenceCheck: item.is_attendence_check
    })
    byDate.set(isoDate, activities)
  }

  const rows: ScheduleRow[] = []
  for (const [isoDate, activities] of byDate) {
    activities.sort((a, b) => a.startAt.localeCompare(b.startAt))
    const rowDate = toRowDate(isoDate)
    rows.push({
      monthKey: buildMonthKey(rowDate),
      dayName: parseDayName(rowDate),
      date: rowDate,
      activities
    })
  }

  rows.sort((a, b) => toSortableDate(a.date).localeCompare(toSortableDate(b.date)))
  return rows
}

async function loadSchedules() {
  loadStatus.value = 'pending'
  try {
    const result = await listGeneralSchedules({})
    schedules.splice(0, schedules.length, ...mapApiRows(result.data ?? []))
    loadStatus.value = 'success'
    await nextTick(expandCurrentMonthGroup)
  } catch {
    loadStatus.value = 'error'
  }
}

function onCreateActivity(activity: ScheduleActivity) {
  const rowDate = toRowDate(activity.startAt.slice(0, 10))
  const existing = schedules.find(row => row.date === rowDate)

  if (existing) {
    existing.activities.push(activity)
    existing.activities.sort((a, b) => a.startAt.localeCompare(b.startAt))
    return
  }

  const newRow: ScheduleRow = {
    monthKey: buildMonthKey(rowDate),
    dayName: parseDayName(rowDate),
    date: rowDate,
    activities: [activity]
  }

  const insertIndex = schedules.findIndex(row => toSortableDate(row.date) > toSortableDate(rowDate))
  if (insertIndex === -1) {
    schedules.push(newRow)
  } else {
    schedules.splice(insertIndex, 0, newRow)
  }
}

function onEditActivity(activity: ScheduleActivity) {
  duplicateMode.value = false
  editingActivityId.value = activity.id
  dialogOpen.value = true
}

function onDuplicateActivity(activity: ScheduleActivity) {
  duplicateMode.value = true
  editingActivityId.value = activity.id
  dialogOpen.value = true
}

// Create-mode trigger lives inside the dialog; clear the edit target on
// close so reopening via the dialog's own "+" button starts a fresh create.
watch(dialogOpen, (isOpen) => {
  if (!isOpen) {
    editingActivityId.value = null
    duplicateMode.value = false
  }
})

function onDeleteActivity(activity: ScheduleActivity) {
  // Not cleared on close — the dialog fades out still showing this activity.
  deletingActivity.value = activity
  deleteDialogOpen.value = true
}

function onDeletedActivity(activity: ScheduleActivity) {
  for (const row of schedules) {
    const index = row.activities.findIndex(item => item.id === activity.id)
    if (index !== -1) {
      row.activities.splice(index, 1)
      break
    }
  }
  const emptyIndex = schedules.findIndex(row => row.activities.length === 0)
  if (emptyIndex !== -1) schedules.splice(emptyIndex, 1)
}

function onUpdateActivity(activity: ScheduleActivity) {
  for (const row of schedules) {
    const index = row.activities.findIndex(item => item.id === activity.id)
    if (index !== -1) {
      row.activities.splice(index, 1)
      break
    }
  }
  const emptyIndex = schedules.findIndex(row => row.activities.length === 0)
  if (emptyIndex !== -1) schedules.splice(emptyIndex, 1)
  onCreateActivity(activity)
}

const groupingOptions = ref<GroupingOptions>({
  groupedColumnMode: 'remove',
  getGroupedRowModel: getGroupedRowModel()
})

const now = new Date()
const currentMonthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`

interface GroupRowLike {
  getIsGrouped: () => boolean
  groupingValue?: unknown
  subRows?: { original: ScheduleRow }[]
  getIsExpanded: () => boolean
  toggleExpanded: (expanded?: boolean) => void
}

function expandCurrentMonthGroup() {
  const api = table.value?.tableApi
  if (!api) return
  const groupRow = (api.getRowModel().rows as GroupRowLike[]).find((row) => {
    if (!row.getIsGrouped()) return false
    return row.groupingValue === currentMonthKey
      || row.subRows?.[0]?.original.monthKey === currentMonthKey
  })
  if (groupRow && !groupRow.getIsExpanded()) {
    groupRow.toggleExpanded(true)
  }
}

onMounted(() => {
  loadSchedules()
})

const columns: TableColumn<ScheduleRow>[] = [
  {
    id: 'title',
    header: 'Tháng',
    meta: {
      class: {
        th: 'w-56',
        td: 'w-56'
      }
    }
  },
  {
    accessorKey: 'monthKey',
    header: 'Month'
  },
  {
    accessorKey: 'dayName',
    header: 'Ngày',
    meta: {
      class: {
        th: 'w-24',
        td: 'w-24'
      }
    }
  },
  {
    accessorKey: 'date',
    header: '',
    meta: {
      class: {
        th: 'w-24',
        td: 'w-24'
      }
    }
  },
  {
    id: 'time',
    header: t('studyYearSchedules.columns.time'),
    meta: {
      class: {
        th: 'w-72',
        td: 'w-72'
      }
    }
  },
  {
    accessorKey: 'activities',
    header: 'Hoạt động',
    meta: {
      class: {
        td: 'w-full'
      }
    }
  },
  {
    id: 'attendance',
    header: t('studyYearSchedules.columns.attendance'),
    meta: {
      class: {
        th: 'w-40 text-xs whitespace-nowrap',
        td: 'w-40 text-xs'
      }
    }
  },
  {
    id: 'actions',
    header: '',
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
      <UDashboardNavbar :title="t('menu.studyYear.schedules')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <StudyYearAddScheduleDayDialog
            v-model:open="dialogOpen"
            :activity-id="editingActivityId"
            :duplicate="duplicateMode"
            @create="onCreateActivity"
            @update="onUpdateActivity"
          />

          <StudyYearDeleteScheduleDayDialog
            v-model:open="deleteDialogOpen"
            :activity="deletingActivity"
            @delete="onDeletedActivity"
          />
        </template>
      </UDashboardNavbar>

      <!-- <UDashboardToolbar /> -->
    </template>

    <template #body>
      <div class="flex shrink-0 flex-wrap items-center justify-between gap-1.5">
        <UInput
          v-model="search"
          class="max-w-sm"
          icon="i-lucide-search"
          placeholder="Tìm trong lịch sinh hoạt"
        />

        <div class="flex items-center gap-1.5">
          <UButton
            :label="expandLabel"
            color="neutral"
            variant="outline"
            :icon="expandIcon"
            @click="toggleExpandAll"
          />
        </div>
      </div>

      <div
        v-if="loadStatus === 'error'"
        class="flex shrink-0 items-center gap-2 text-sm text-error"
      >
        <span>{{ t('studyYearSchedules.loadError') }}</span>
        <UButton
          :label="t('studyYearSchedules.retry')"
          color="error"
          variant="soft"
          size="xs"
          @click="loadSchedules"
        />
      </div>

      <div
        v-if="loadStatus === 'pending'"
        class="space-y-2"
        aria-busy="true"
      >
        <!-- Same columns/widths as the table: Tháng | Ngày | date | Thời gian | Hoạt động | Điểm danh | actions -->
        <div
          v-for="n in 9"
          :key="n"
          class="flex items-center gap-4"
        >
          <USkeleton class="h-12 w-56 shrink-0" />
          <USkeleton class="h-12 w-24 shrink-0" />
          <USkeleton class="h-12 w-24 shrink-0" />
          <USkeleton class="h-12 w-72 shrink-0" />
          <USkeleton class="h-12 w-full grow" />
          <USkeleton class="h-12 w-40 shrink-0" />
          <USkeleton class="h-12 w-28 shrink-0" />
        </div>
      </div>

      <UTable
        v-else
        ref="table"
        sticky="header"
        class="min-h-0 flex-1"
        :data="filteredSchedules"
        :columns="columns"
        :grouping="['monthKey']"
        :grouping-options="groupingOptions"
        :expanded-options="{ autoResetExpanded: false }"
        :ui="{
          root: 'my-0',
          base: 'table-fixed border-separate border-spacing-0 h-full',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none [&>tr>th]:bg-elevated',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-2 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r text-sm',
          td: ' border-b border-default empty:p-0 empty:border-0 text-sm',
          separator: 'h-0'
        }"
      >
        <template #title-cell="{ row }">
          <div v-if="row.getIsGrouped()" class="flex items-center gap-2">
            <UButton
              color="neutral"
              variant="outline"
              size="xs"
              :icon="row.getIsExpanded() ? 'i-lucide-minus' : 'i-lucide-plus'"
              @click="row.toggleExpanded()"
            />
            <span class="font-semibold text-highlighted">
              {{ formatMonthLabel(row.original.monthKey) }}
            </span>
            <span class="text-sm text-muted">
              ({{ row.subRows?.length ?? 0 }} {{ (row.subRows?.length ?? 0) <= 1 ? 'ngày' : 'ngày' }})
            </span>
          </div>
          <!-- <div v-else>
            <div class="font-semibold text-highlighted">{{ row.original.dayName }}</div>
            <div class="text-sm text-muted">{{ row.original.date }}</div>
          </div> -->
        </template>

        <template #monthKey-cell>
          <!-- hidden: used only for grouping -->
        </template>

        <template #dayName-cell="{ row }">
          <span v-if="!row.getIsGrouped()" class="font-semibold text-highlighted">
            {{ row.original.dayName }}
          </span>
        </template>

        <template #date-cell="{ row }">
          <span v-if="!row.getIsGrouped()" class="text-muted">
            {{ row.original.date }}
          </span>
        </template>

        <template #time-cell="{ row }">
          <div v-if="!row.getIsGrouped()">
            <div
              v-if="row.original.activities.length === 0"
              class="text-dimmed"
            >
              —
            </div>
            <div
              v-for="(activity, i) in row.original.activities"
              :key="i"
              class="flex h-6 items-center text-muted"
            >
              {{ formatTimeRange(activity) }}
            </div>
          </div>
        </template>

        <template #activities-cell="{ row }">
          <div v-if="!row.getIsGrouped()">
            <div
              v-if="row.original.activities.length === 0"
              class="text-dimmed"
            >
              —
            </div>
            <div
              v-for="activity in row.original.activities"
              :key="activity.id"
              class="flex min-h-6 items-center gap-2"
            >
              <span
                class="h-2 w-2 shrink-0 rounded-full"
                :style="{ backgroundColor: activity.color }"
              />
              <span class="min-w-0 break-words whitespace-normal">{{ activity.activityTypeName }} - {{ activity.name }}</span>
            </div>
          </div>
        </template>

        <template #attendance-cell="{ row }">
          <div v-if="!row.getIsGrouped()">
            <div
              v-if="row.original.activities.length === 0"
              class="text-dimmed"
            >
              —
            </div>
            <div
              v-for="activity in row.original.activities"
              :key="activity.id"
              class="flex h-6 items-center"
            >
              <UBadge
                :color="activity.isAttendenceCheck ? 'success' : 'neutral'"
                variant="subtle"
                size="sm"
              >
                {{ activity.isAttendenceCheck ? t('common.yes') : t('common.no') }}
              </UBadge>
            </div>
          </div>
        </template>

        <template #actions-cell="{ row }">
          <div v-if="!row.getIsGrouped()">
            <div
              v-for="activity in row.original.activities"
              :key="activity.id"
              class="flex h-6 items-center justify-end gap-1"
            >
              <UTooltip :text="t('studyYearSchedules.actions.edit')">
                <UButton
                  icon="i-lucide-pencil"
                  color="neutral"
                  variant="ghost"
                  size="xs"
                  :aria-label="t('studyYearSchedules.actions.edit')"
                  @click="onEditActivity(activity)"
                />
              </UTooltip>
              <UTooltip :text="t('studyYearSchedules.actions.duplicate')">
                <UButton
                  icon="i-lucide-copy"
                  color="neutral"
                  variant="ghost"
                  size="xs"
                  :aria-label="t('studyYearSchedules.actions.duplicate')"
                  @click="onDuplicateActivity(activity)"
                />
              </UTooltip>
              <UTooltip :text="t('studyYearSchedules.actions.delete')">
                <UButton
                  icon="i-lucide-trash-2"
                  color="error"
                  variant="ghost"
                  size="xs"
                  :aria-label="t('studyYearSchedules.actions.delete')"
                  @click="onDeleteActivity(activity)"
                />
              </UTooltip>
            </div>
          </div>
        </template>
      </UTable>
    </template>
  </UDashboardPanel>
</template>
