<script setup lang="ts">
import * as z from 'zod'
import type { CalendarDate } from '@internationalized/date'
import type { FormSubmitEvent } from '@nuxt/ui'
import { listScheduleActivityTypes, syncGradeSchedules } from '~/generated-client'

const { t } = useI18n()
const toast = useToast()

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{ gradeId: string }>()

const emit = defineEmits<{
  synced: []
}>()

interface ActivityTypeOption {
  id: number
  label: string
  color: string
}

const activityTypes = ref<ActivityTypeOption[]>([])
const activityTypesStatus = ref<'pending' | 'success' | 'error'>('pending')

async function loadActivityTypes() {
  activityTypesStatus.value = 'pending'
  try {
    const result = await listScheduleActivityTypes({})
    activityTypes.value = (result.data ?? []).map(item => ({
      id: item.id,
      label: item.name,
      color: toCssColor(item.color)
    }))
    activityTypesStatus.value = 'success'
  } catch {
    activityTypesStatus.value = 'error'
  }
}

onMounted(loadActivityTypes)

const schema = z.object({
  activityTypeIds: z
    .array(z.number())
    .min(1, t('gradeSchedules.sync.validation.activityTypesRequired')),
  syncDate: z.boolean(),
  syncName: z.boolean(),
  syncStartTime: z.boolean(),
  syncEndTime: z.boolean()
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  activityTypeIds: [],
  syncDate: true,
  syncName: true,
  syncStartTime: true,
  syncEndTime: true
})

// Optional date range — both empty means "all".
const rangeStart = ref<CalendarDate | undefined>()
const rangeEnd = ref<CalendarDate | undefined>()

const displayRange = computed(() => {
  if (!rangeStart.value) return t('gradeSchedules.sync.dateRangeAll')
  const start = formatCalendarDate(rangeStart.value)
  if (!rangeEnd.value) return start
  return `${start} - ${formatCalendarDate(rangeEnd.value)}`
})

function formatCalendarDate(value: CalendarDate) {
  return `${String(value.day).padStart(2, '0')}/${String(value.month).padStart(2, '0')}/${value.year}`
}

const calendarRange = computed({
  get: () => ({
    start: rangeStart.value ?? undefined,
    end: rangeEnd.value ?? undefined
  }),
  set: (value: { start?: CalendarDate | null, end?: CalendarDate | null }) => {
    rangeStart.value = value.start ?? undefined
    // Range calendar emits a partial range while the user is still picking.
    rangeEnd.value = value.end ?? undefined
  }
})

function clearRange() {
  rangeStart.value = undefined
  rangeEnd.value = undefined
}

function reset() {
  state.activityTypeIds = []
  state.syncDate = true
  state.syncName = true
  state.syncStartTime = true
  state.syncEndTime = true
  clearRange()
}

const submitting = ref(false)

watch(open, (isOpen) => {
  if (isOpen) reset()
})

function cancel() {
  open.value = false
}

async function onSubmit(event: FormSubmitEvent<Schema>) {
  if (submitting.value) return
  submitting.value = true
  try {
    const result = await syncGradeSchedules({
      body: {
        grade_id: props.gradeId,
        date_from: rangeStart.value ? rangeStart.value.toString().slice(0, 10) : null,
        // Start picked without end = that single day; both empty = all.
        date_to: rangeEnd.value
          ? rangeEnd.value.toString().slice(0, 10)
          : rangeStart.value
            ? rangeStart.value.toString().slice(0, 10)
            : null,
        schedule_activity_type_ids: event.data.activityTypeIds,
        sync_date: event.data.syncDate,
        sync_name: event.data.syncName,
        sync_start_time: event.data.syncStartTime,
        sync_end_time: event.data.syncEndTime
      }
    })
    toast.add({
      title: t('gradeSchedules.sync.success', {
        created: result.created,
        updated: result.updated
      }),
      color: 'success'
    })
    emit('synced')
    open.value = false
  } catch {
    toast.add({
      title: t('gradeSchedules.sync.failed'),
      color: 'error'
    })
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <UModal
    v-model:open="open"
    :title="t('gradeSchedules.sync.title')"
    :dismissible="!submitting"
  >
    <template #body>
      <UForm
        :schema="schema"
        :state="state"
        :disabled="submitting"
        class="space-y-4"
        @submit="onSubmit"
      >
        <UFormField
          :label="t('gradeSchedules.sync.dateRange')"
          name="dateRange"
        >
          <div class="flex items-center gap-2">
            <UPopover :content="{ align: 'start' }">
              <UButton
                type="button"
                color="neutral"
                variant="outline"
                trailing-icon="i-lucide-calendar"
                :label="displayRange"
                class="min-w-64 justify-between"
                :disabled="submitting"
              />
              <template #content>
                <div class="flex flex-col">
                  <UCalendar
                    v-model="calendarRange"
                    locale="vi"
                    :number-of-months="2"
                    range
                  />
                  <div class="flex justify-end border-t border-default p-2">
                    <UButton
                      type="button"
                      color="neutral"
                      variant="ghost"
                      size="xs"
                      :label="t('gradeSchedules.sync.clearRange')"
                      :disabled="submitting"
                      @click="clearRange"
                    />
                  </div>
                </div>
              </template>
            </UPopover>
          </div>
        </UFormField>

        <UFormField
          :label="t('gradeSchedules.sync.activityTypes')"
          name="activityTypeIds"
          required
        >
          <USelectMenu
            v-model="state.activityTypeIds"
            :items="activityTypes"
            value-key="id"
            multiple
            :placeholder="t('gradeSchedules.sync.activityTypesPlaceholder')"
            :loading="activityTypesStatus === 'pending'"
            :disabled="activityTypesStatus !== 'success'"
            class="w-full"
          >
            <template #item="{ item }">
              <div class="flex items-center gap-2">
                <span
                  class="block h-2 w-2 shrink-0 rounded-full"
                  :style="{ backgroundColor: item.color }"
                />
                <span class="truncate">{{ item.label }}</span>
              </div>
            </template>
          </USelectMenu>
        </UFormField>

        <div
          v-if="activityTypesStatus === 'error'"
          class="flex items-center gap-2 text-sm text-error"
        >
          <span>{{ t('gradeSchedules.sync.activityTypesLoadError') }}</span>
          <UButton
            :label="t('gradeSchedules.sync.retry')"
            color="error"
            variant="soft"
            size="xs"
            @click="loadActivityTypes"
          />
        </div>

        <UFormField
          :label="t('gradeSchedules.sync.syncFields')"
          name="syncFields"
        >
          <div class="flex flex-wrap gap-x-6 gap-y-2">
            <UCheckbox
              v-model="state.syncDate"
              :label="t('gradeSchedules.sync.fields.date')"
              :disabled="submitting"
            />
            <UCheckbox
              v-model="state.syncName"
              :label="t('gradeSchedules.sync.fields.name')"
              :disabled="submitting"
            />
            <UCheckbox
              v-model="state.syncStartTime"
              :label="t('gradeSchedules.sync.fields.startTime')"
              :disabled="submitting"
            />
            <UCheckbox
              v-model="state.syncEndTime"
              :label="t('gradeSchedules.sync.fields.endTime')"
              :disabled="submitting"
            />
          </div>
        </UFormField>

        <p class="text-xs text-dimmed">
          {{ t('gradeSchedules.sync.note') }}
        </p>

        <div class="flex justify-end gap-2">
          <UButton
            :label="t('gradeSchedules.addDay.cancel')"
            type="button"
            color="neutral"
            variant="subtle"
            :disabled="submitting"
            @click="cancel"
          />
          <UButton
            :label="t('gradeSchedules.sync.submit')"
            type="submit"
            color="primary"
            :loading="submitting"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
