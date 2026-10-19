<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { getGroupedRowModel, type GroupingOptions } from '@tanstack/vue-table'
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
  return formatted.charAt(0).toUpperCase() + formatted.slice(1)
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

const schedules = reactive<ScheduleRow[]>([
  // --- Tháng 10/2026 (existing) ---
  {
    monthKey: buildMonthKey('04-10-2026'),
    dayName: 'Chủ Nhật',
    date: '04-10-2026',
    activities: [
      { color: '#10b981', name: 'Chầu Thánh Thể', startAt: '2026-10-04T08:00', endAt: '2026-10-04T09:00' },
      { color: '#f59e0b', name: 'Luyện tập phụng vụ', startAt: '2026-10-04T09:15', endAt: '2026-10-04T10:30' }
    ]
  },
  {
    monthKey: buildMonthKey('11-10-2026'),
    dayName: 'Chủ Nhật',
    date: '11-10-2026',
    activities: [
      { color: '#ef4444', name: 'Giáo lý lớp 5 - Bí tích', startAt: '2026-10-11T08:00', endAt: '2026-10-11T09:00' },
      { color: '#3b82f6', name: 'Thánh lễ thiếu nhi', startAt: '2026-10-11T09:30', endAt: '2026-10-11T10:30' }
    ]
  },
  {
    monthKey: buildMonthKey('18-10-2026'),
    dayName: 'Chủ Nhật',
    date: '18-10-2026',
    activities: []
  },
  {
    monthKey: buildMonthKey('25-10-2026'),
    dayName: 'Chủ Nhật',
    date: '25-10-2026',
    activities: [
      { color: '#8b5cf6', name: 'Giáo lý sau Thánh lễ', startAt: '2026-10-25T10:45', endAt: '2026-10-25T11:30' },
      { color: '#10b981', name: 'Bài hát phụng vụ', startAt: '2026-10-25T13:00' }
    ]
  },
  // --- Tháng 11/2026: 4 Sundays ---
  {
    monthKey: buildMonthKey('01-11-2026'),
    dayName: 'Chủ Nhật',
    date: '01-11-2026',
    activities: [
      { color: '#f59e0b', name: 'Huấn luyện đội ngũ giáo lý viên', startAt: '2026-11-01T08:00', endAt: '2026-11-01T10:00' },
      { color: '#ef4444', name: 'Giáo lý lớp 2 - Bí tích Thánh Thể', startAt: '2026-11-01T10:15', endAt: '2026-11-01T11:15' }
    ]
  },
  {
    monthKey: buildMonthKey('08-11-2026'),
    dayName: 'Chủ Nhật',
    date: '08-11-2026',
    activities: [
      { color: '#3b82f6', name: 'Kinh Thánh - Giáo lý lớp 1', startAt: '2026-11-08T09:00' }
    ]
  },
  {
    monthKey: buildMonthKey('15-11-2026'),
    dayName: 'Chủ Nhật',
    date: '15-11-2026',
    activities: [
      { color: '#10b981', name: 'Chầu Thánh Thể', startAt: '2026-11-15T08:00', endAt: '2026-11-15T09:00' },
      { color: '#8b5cf6', name: 'Giáo lý lớp 3 - Kinh Mân Côi', startAt: '2026-11-15T09:15', endAt: '2026-11-15T10:15' }
    ]
  },
  {
    monthKey: buildMonthKey('22-11-2026'),
    dayName: 'Chủ Nhật',
    date: '22-11-2026',
    activities: [
      { color: '#3b82f6', name: 'Thánh lễ thiếu nhi', startAt: '2026-11-22T09:30', endAt: '2026-11-22T10:30' },
      { color: '#f59e0b', name: 'Luyện tập phụng vụ', startAt: '2026-11-22T10:45', endAt: '2026-11-22T12:00' },
      { color: '#ef4444', name: 'Giáo lý lớp 4 - Thánh Kinh', startAt: '2026-11-22T13:00', endAt: '2026-11-22T14:00' }
    ]
  },
  // --- Tháng 12/2026: NO DATA ---
  // --- Tháng 01/2027: 2 of 5 Sundays ---
  {
    monthKey: buildMonthKey('03-01-2027'),
    dayName: 'Chủ Nhật',
    date: '03-01-2027',
    activities: [
      { color: '#3b82f6', name: 'Thánh lễ thiếu nhi', startAt: '2027-01-03T09:30', endAt: '2027-01-03T10:30' },
      { color: '#8b5cf6', name: 'Giáo lý sau Thánh lễ', startAt: '2027-01-03T10:45', endAt: '2027-01-03T11:30' }
    ]
  },
  {
    monthKey: buildMonthKey('17-01-2027'),
    dayName: 'Chủ Nhật',
    date: '17-01-2027',
    activities: [
      { color: '#10b981', name: 'Bài hát phụng vụ', startAt: '2027-01-17T13:00', endAt: '2027-01-17T14:00' }
    ]
  },
  // --- Tháng 02/2027: 2 of 4 Sundays ---
  {
    monthKey: buildMonthKey('07-02-2027'),
    dayName: 'Chủ Nhật',
    date: '07-02-2027',
    activities: [
      { color: '#ef4444', name: 'Giáo lý lớp 2 - Bí tích Thánh Thể', startAt: '2027-02-07T08:00', endAt: '2027-02-07T09:00' },
      { color: '#3b82f6', name: 'Kinh Thánh - Giáo lý lớp 1', startAt: '2027-02-07T09:15', endAt: '2027-02-07T10:15' }
    ]
  },
  {
    monthKey: buildMonthKey('21-02-2027'),
    dayName: 'Chủ Nhật',
    date: '21-02-2027',
    activities: [
      { color: '#f59e0b', name: 'Huấn luyện đội ngũ giáo lý viên', startAt: '2027-02-21T08:00' }
    ]
  },
  // --- Tháng 03/2027: all 4 Sundays ---
  {
    monthKey: buildMonthKey('07-03-2027'),
    dayName: 'Chủ Nhật',
    date: '07-03-2027',
    activities: [
      { color: '#10b981', name: 'Chầu Thánh Thể', startAt: '2027-03-07T08:00', endAt: '2027-03-07T09:00' },
      { color: '#f59e0b', name: 'Luyện tập phụng vụ', startAt: '2027-03-07T09:15', endAt: '2027-03-07T10:30' }
    ]
  },
  {
    monthKey: buildMonthKey('14-03-2027'),
    dayName: 'Chủ Nhật',
    date: '14-03-2027',
    activities: [
      { color: '#8b5cf6', name: 'Giáo lý lớp 3 - Kinh Mân Côi', startAt: '2027-03-14T08:00', endAt: '2027-03-14T09:00' },
      { color: '#ef4444', name: 'Giáo lý lớp 5 - Bí tích', startAt: '2027-03-14T09:15', endAt: '2027-03-14T10:15' }
    ]
  },
  {
    monthKey: buildMonthKey('21-03-2027'),
    dayName: 'Chủ Nhật',
    date: '21-03-2027',
    activities: [
      { color: '#3b82f6', name: 'Thánh lễ thiếu nhi', startAt: '2027-03-21T09:30', endAt: '2027-03-21T10:30' },
      { color: '#10b981', name: 'Bài hát phụng vụ', startAt: '2027-03-21T10:45', endAt: '2027-03-21T11:30' },
      { color: '#8b5cf6', name: 'Giáo lý sau Thánh lễ', startAt: '2027-03-21T11:30', endAt: '2027-03-21T12:00' }
    ]
  },
  {
    monthKey: buildMonthKey('28-03-2027'),
    dayName: 'Chủ Nhật',
    date: '28-03-2027',
    activities: []
  },
  // --- Tháng 04/2027: 2 of 4 Sundays ---
  {
    monthKey: buildMonthKey('04-04-2027'),
    dayName: 'Chủ Nhật',
    date: '04-04-2027',
    activities: [
      { color: '#3b82f6', name: 'Kinh Thánh - Giáo lý lớp 1', startAt: '2027-04-04T09:15', endAt: '2027-04-04T10:15' }
    ]
  },
  {
    monthKey: buildMonthKey('25-04-2027'),
    dayName: 'Chủ Nhật',
    date: '25-04-2027',
    activities: [
      { color: '#ef4444', name: 'Giáo lý lớp 4 - Thánh Kinh', startAt: '2027-04-25T13:00', endAt: '2027-04-25T14:00' },
      { color: '#f59e0b', name: 'Luyện tập phụng vụ', startAt: '2027-04-25T14:15', endAt: '2027-04-25T15:30' }
    ]
  },
  // --- Tháng 05/2027: 3 of 5 Sundays ---
  {
    monthKey: buildMonthKey('02-05-2027'),
    dayName: 'Chủ Nhật',
    date: '02-05-2027',
    activities: [
      { color: '#10b981', name: 'Chầu Thánh Thể', startAt: '2027-05-02T08:00' }
    ]
  },
  {
    monthKey: buildMonthKey('16-05-2027'),
    dayName: 'Chủ Nhật',
    date: '16-05-2027',
    activities: [
      { color: '#3b82f6', name: 'Thánh lễ thiếu nhi', startAt: '2027-05-16T09:30', endAt: '2027-05-16T10:30' },
      { color: '#8b5cf6', name: 'Giáo lý sau Thánh lễ', startAt: '2027-05-16T10:45', endAt: '2027-05-16T11:30' }
    ]
  },
  {
    monthKey: buildMonthKey('30-05-2027'),
    dayName: 'Chủ Nhật',
    date: '30-05-2027',
    activities: [
      { color: '#ef4444', name: 'Giáo lý lớp 2 - Bí tích Thánh Thể', startAt: '2027-05-30T08:00', endAt: '2027-05-30T09:00' },
      { color: '#f59e0b', name: 'Huấn luyện đội ngũ giáo lý viên', startAt: '2027-05-30T09:15', endAt: '2027-05-30T10:15' },
      { color: '#10b981', name: 'Bài hát phụng vụ', startAt: '2027-05-30T13:00', endAt: '2027-05-30T14:00' }
    ]
  }
])

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
  nextTick(expandCurrentMonthGroup)
})

const columns: TableColumn<ScheduleRow>[] = [
  {
    id: 'title',
    header: 'Tháng'
  },
  {
    accessorKey: 'monthKey',
    header: 'Month'
  },
  {
    accessorKey: 'dayName',
    header: 'Ngày'
  },
  {
    accessorKey: 'date',
    header: ''
  },
  {
    id: 'time',
    header: t('studyYearSchedules.columns.time'),
    meta: {
      class: {
        th: 'w-40',
        td: 'w-40'
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
          <StudyYearAddScheduleDayDialog @create="onCreateActivity" />
        </template>
      </UDashboardNavbar>

      <!-- <UDashboardToolbar /> -->
    </template>

    <template #body>
      <div class="flex flex-wrap items-center justify-between gap-1.5">
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

      <UTable
        ref="table"
        :data="filteredSchedules"
        :columns="columns"
        :grouping="['monthKey']"
        :grouping-options="groupingOptions"
        :expanded-options="{ autoResetExpanded: false }"
        :ui="{
          base: 'table-fixed border-separate border-spacing-0',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-1.5 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r text-xs',
          td: 'py-1.5 border-b border-default empty:p-0 empty:border-0 text-xs',
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
            <span class="text-xs text-muted">
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
          <span v-if="!row.getIsGrouped()" class="text-sm text-muted">
            {{ row.original.date }}
          </span>
        </template>

        <template #time-cell="{ row }">
          <div v-if="!row.getIsGrouped()">
            <div
              v-if="row.original.activities.length === 0"
              class="text-sm text-dimmed"
            >
              —
            </div>
            <div
              v-for="(activity, i) in row.original.activities"
              :key="i"
              class="text-sm text-muted"
            >
              {{ formatTimeRange(activity) }}
            </div>
          </div>
        </template>

        <template #activities-cell="{ row }">
          <div v-if="!row.getIsGrouped()">
            <div
              v-if="row.original.activities.length === 0"
              class="text-sm text-dimmed"
            >
              —
            </div>
            <div
              v-for="(activity, i) in row.original.activities"
              :key="i"
              class="flex items-start gap-2"
            >
              <span
                class="mt-1.5 h-2 w-2 shrink-0 rounded-full"
                :style="{ backgroundColor: activity.color }"
              />
              <span class="text-sm">{{ activity.name }}</span>
            </div>
          </div>
        </template>
      </UTable>
    </template>
  </UDashboardPanel>
</template>
