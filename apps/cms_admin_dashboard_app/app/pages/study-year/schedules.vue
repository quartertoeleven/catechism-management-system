<script setup lang="ts">
import type { TableColumn } from '@nuxt/ui'
import { getGroupedRowModel, type GroupingOptions } from '@tanstack/vue-table'

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
    (row) =>
      row.date.includes(q)
      || row.activities.some((a) => a.description.toLowerCase().includes(q)),
  )
})

interface ScheduleActivity {
  color: string
  description: string
}

interface ScheduleRow {
  monthKey: string
  dayName: string
  date: string
  activities: ScheduleActivity[]
}

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

const schedules: ScheduleRow[] = [
  // --- Tháng 10/2026 (existing) ---
  {
    monthKey: buildMonthKey('04-10-2026'),
    dayName: 'Chủ Nhật',
    date: '04-10-2026',
    activities: [
      { color: '#10b981', description: 'Chầu Thánh Thể' },
      { color: '#f59e0b', description: 'Luyện tập phụng vụ' },
    ],
  },
  {
    monthKey: buildMonthKey('11-10-2026'),
    dayName: 'Chủ Nhật',
    date: '11-10-2026',
    activities: [
      { color: '#ef4444', description: 'Giáo lý lớp 5 - Bí tích' },
      { color: '#3b82f6', description: 'Thánh lễ thiếu nhi' },
    ],
  },
  {
    monthKey: buildMonthKey('18-10-2026'),
    dayName: 'Chủ Nhật',
    date: '18-10-2026',
    activities: [],
  },
  {
    monthKey: buildMonthKey('25-10-2026'),
    dayName: 'Chủ Nhật',
    date: '25-10-2026',
    activities: [
      { color: '#8b5cf6', description: 'Giáo lý sau Thánh lễ' },
      { color: '#10b981', description: 'Bài hát phụng vụ' },
    ],
  },
  // --- Tháng 11/2026: 4 Sundays ---
  {
    monthKey: buildMonthKey('01-11-2026'),
    dayName: 'Chủ Nhật',
    date: '01-11-2026',
    activities: [
      { color: '#f59e0b', description: 'Huấn luyện đội ngũ giáo lý viên' },
      { color: '#ef4444', description: 'Giáo lý lớp 2 - Bí tích Thánh Thể' },
    ],
  },
  {
    monthKey: buildMonthKey('08-11-2026'),
    dayName: 'Chủ Nhật',
    date: '08-11-2026',
    activities: [
      { color: '#3b82f6', description: 'Kinh Thánh - Giáo lý lớp 1' },
    ],
  },
  {
    monthKey: buildMonthKey('15-11-2026'),
    dayName: 'Chủ Nhật',
    date: '15-11-2026',
    activities: [
      { color: '#10b981', description: 'Chầu Thánh Thể' },
      { color: '#8b5cf6', description: 'Giáo lý lớp 3 - Kinh Mân Côi' },
    ],
  },
  {
    monthKey: buildMonthKey('22-11-2026'),
    dayName: 'Chủ Nhật',
    date: '22-11-2026',
    activities: [
      { color: '#3b82f6', description: 'Thánh lễ thiếu nhi' },
      { color: '#f59e0b', description: 'Luyện tập phụng vụ' },
      { color: '#ef4444', description: 'Giáo lý lớp 4 - Thánh Kinh' },
    ],
  },
  // --- Tháng 12/2026: NO DATA ---
  // --- Tháng 01/2027: 2 of 5 Sundays ---
  {
    monthKey: buildMonthKey('03-01-2027'),
    dayName: 'Chủ Nhật',
    date: '03-01-2027',
    activities: [
      { color: '#3b82f6', description: 'Thánh lễ thiếu nhi' },
      { color: '#8b5cf6', description: 'Giáo lý sau Thánh lễ' },
    ],
  },
  {
    monthKey: buildMonthKey('17-01-2027'),
    dayName: 'Chủ Nhật',
    date: '17-01-2027',
    activities: [
      { color: '#10b981', description: 'Bài hát phụng vụ' },
    ],
  },
  // --- Tháng 02/2027: 2 of 4 Sundays ---
  {
    monthKey: buildMonthKey('07-02-2027'),
    dayName: 'Chủ Nhật',
    date: '07-02-2027',
    activities: [
      { color: '#ef4444', description: 'Giáo lý lớp 2 - Bí tích Thánh Thể' },
      { color: '#3b82f6', description: 'Kinh Thánh - Giáo lý lớp 1' },
    ],
  },
  {
    monthKey: buildMonthKey('21-02-2027'),
    dayName: 'Chủ Nhật',
    date: '21-02-2027',
    activities: [
      { color: '#f59e0b', description: 'Huấn luyện đội ngũ giáo lý viên' },
    ],
  },
  // --- Tháng 03/2027: all 4 Sundays ---
  {
    monthKey: buildMonthKey('07-03-2027'),
    dayName: 'Chủ Nhật',
    date: '07-03-2027',
    activities: [
      { color: '#10b981', description: 'Chầu Thánh Thể' },
      { color: '#f59e0b', description: 'Luyện tập phụng vụ' },
    ],
  },
  {
    monthKey: buildMonthKey('14-03-2027'),
    dayName: 'Chủ Nhật',
    date: '14-03-2027',
    activities: [
      { color: '#8b5cf6', description: 'Giáo lý lớp 3 - Kinh Mân Côi' },
      { color: '#ef4444', description: 'Giáo lý lớp 5 - Bí tích' },
    ],
  },
  {
    monthKey: buildMonthKey('21-03-2027'),
    dayName: 'Chủ Nhật',
    date: '21-03-2027',
    activities: [
      { color: '#3b82f6', description: 'Thánh lễ thiếu nhi' },
      { color: '#10b981', description: 'Bài hát phụng vụ' },
      { color: '#8b5cf6', description: 'Giáo lý sau Thánh lễ' },
    ],
  },
  {
    monthKey: buildMonthKey('28-03-2027'),
    dayName: 'Chủ Nhật',
    date: '28-03-2027',
    activities: [],
  },
  // --- Tháng 04/2027: 2 of 4 Sundays ---
  {
    monthKey: buildMonthKey('04-04-2027'),
    dayName: 'Chủ Nhật',
    date: '04-04-2027',
    activities: [
      { color: '#3b82f6', description: 'Kinh Thánh - Giáo lý lớp 1' },
    ],
  },
  {
    monthKey: buildMonthKey('25-04-2027'),
    dayName: 'Chủ Nhật',
    date: '25-04-2027',
    activities: [
      { color: '#ef4444', description: 'Giáo lý lớp 4 - Thánh Kinh' },
      { color: '#f59e0b', description: 'Luyện tập phụng vụ' },
    ],
  },
  // --- Tháng 05/2027: 3 of 5 Sundays ---
  {
    monthKey: buildMonthKey('02-05-2027'),
    dayName: 'Chủ Nhật',
    date: '02-05-2027',
    activities: [
      { color: '#10b981', description: 'Chầu Thánh Thể' },
    ],
  },
  {
    monthKey: buildMonthKey('16-05-2027'),
    dayName: 'Chủ Nhật',
    date: '16-05-2027',
    activities: [
      { color: '#8b5cf6', description: 'Giáo lý sau Thánh lễ' },
      { color: '#3b82f6', description: 'Thánh lễ thiếu nhi' },
    ],
  },
  {
    monthKey: buildMonthKey('30-05-2027'),
    dayName: 'Chủ Nhật',
    date: '30-05-2027',
    activities: [
      { color: '#ef4444', description: 'Giáo lý lớp 2 - Bí tích Thánh Thể' },
      { color: '#f59e0b', description: 'Huấn luyện đội ngũ giáo lý viên' },
      { color: '#10b981', description: 'Bài hát phụng vụ' },
    ],
  },
]

const groupingOptions = ref<GroupingOptions>({
  groupedColumnMode: 'remove',
  getGroupedRowModel: getGroupedRowModel(),
})

const columns: TableColumn<ScheduleRow>[] = [
  {
    id: 'title',
    header: 'Tháng',
  },
  {
    accessorKey: 'monthKey',
    header: 'Month',
  },
  {
    accessorKey: 'dayName',
    header: 'Ngày',
  },
  {
    accessorKey: 'date',
    header: '',
  },
  {
    accessorKey: 'activities',
    header: 'Hoạt động',
    meta: {
      class: {
        td: 'w-full',
      },
    },
  },
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
          <UButton
            label="Thêm ngày sinh hoạt"
            icon="i-lucide-plus"
          />
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
        :ui="{
          base: 'table-fixed border-separate border-spacing-0',
          thead: '[&>tr]:bg-elevated/50 [&>tr]:after:content-none',
          tbody: '[&>tr]:last:[&>td]:border-b-0',
          th: 'py-1.5 first:rounded-l-lg last:rounded-r-lg border-y border-default first:border-l last:border-r text-xs',
          td: 'py-1.5 border-b border-default empty:p-0 empty:border-0 text-xs',
          separator: 'h-0',
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
              class="flex items-center gap-2"
            >
              <span
                class="h-2 w-2 shrink-0 rounded-full"
                :style="{ backgroundColor: activity.color }"
              />
              <span class="text-sm">{{ activity.description }}</span>
            </div>
          </div>
        </template>
      </UTable>
    </template>
  </UDashboardPanel>
</template>
