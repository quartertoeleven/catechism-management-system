<script setup lang="ts">
import * as z from 'zod'
import { CalendarDate } from '@internationalized/date'
import type { FormSubmitEvent } from '@nuxt/ui'
import { getGeneralSchedule, listScheduleActivityTypes, upsertGeneralSchedule } from '~/generated-client'
import type { ScheduleActivity } from '~/types'

const { t } = useI18n()
const toast = useToast()

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{ activityId?: string | null }>()

const emit = defineEmits<{
  create: [activity: ScheduleActivity]
  update: [activity: ScheduleActivity]
}>()

// Frozen at open time — recomputing from `activityId` while the modal is
// still fading out would flip the title/buttons back to create mode.
const mode = ref<'create' | 'edit'>('create')
const isEditMode = computed(() => mode.value === 'edit')

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
  scheduleActivityTypeId: z.number(t('studyYearSchedules.addDay.validation.activityTypeRequired')),
  name: z.string()
    .min(1, t('studyYearSchedules.addDay.validation.nameRequired'))
    .max(100, t('studyYearSchedules.addDay.validation.nameMax')),
  isAttendenceCheck: z.boolean(),
  date: z.string().min(1, t('studyYearSchedules.addDay.validation.dateRequired')),
  startTime: z.string().min(1, t('studyYearSchedules.addDay.validation.startTimeRequired')),
  endTime: z.string().optional()
}).superRefine((value, ctx) => {
  if (value.endTime && value.endTime <= value.startTime) {
    ctx.addIssue({
      code: 'custom',
      path: ['endTime'],
      message: t('studyYearSchedules.addDay.validation.endTimeAfterStartTime')
    })
  }
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  scheduleActivityTypeId: undefined,
  name: '',
  isAttendenceCheck: true,
  date: '',
  startTime: '',
  endTime: undefined
})

const submitting = ref(false)

// Edit mode: `detail` has no form input — preserved as fetched, never re-sent blank.
const editDetail = ref<string | null>(null)
const loadingDetail = ref(false)

const activityTypeSelect = ref<{ triggerRef?: HTMLElement | null } | null>(null)

const selectedDate = computed({
  get: () => {
    if (!state.date) return undefined
    const [yearStr, monthStr, dayStr] = state.date.split('-')
    return new CalendarDate(Number(yearStr), Number(monthStr), Number(dayStr))
  },
  set: (value) => {
    state.date = value ? value.toString().slice(0, 10) : ''
  }
})

const displayDate = computed(() => {
  if (!state.date) return t('studyYearSchedules.addDay.datePlaceholder')
  const [year, month, day] = state.date.split('-')
  return `${day}/${month}/${year}`
})

function reset() {
  state.scheduleActivityTypeId = undefined
  state.name = ''
  state.date = ''
  state.startTime = ''
  state.endTime = undefined
  state.isAttendenceCheck = true
  editDetail.value = null
}

async function loadDetail() {
  if (!props.activityId) return
  loadingDetail.value = true
  try {
    const result = await getGeneralSchedule({
      path: { schedule_id: props.activityId }
    })
    state.scheduleActivityTypeId = result.schedule_activity_type_id
    state.name = result.name
    state.date = result.start_at.slice(0, 10)
    state.startTime = result.start_at.slice(11, 16)
    state.endTime = result.end_at ? result.end_at.slice(11, 16) : undefined
    state.isAttendenceCheck = result.is_attendence_check
    editDetail.value = result.detail
  } catch {
    toast.add({
      title: t('studyYearSchedules.loadError'),
      color: 'error'
    })
    open.value = false
  } finally {
    loadingDetail.value = false
  }
}

function focusActivityType() {
  // The dialog moves focus to its first focusable element (the close button)
  // after opening — defer past it, then focus the first field's trigger.
  setTimeout(() => {
    const trigger = activityTypeSelect.value?.triggerRef as unknown as HTMLElement | { $el?: HTMLElement } | null | undefined
    const el = trigger instanceof HTMLElement ? trigger : trigger?.$el
    el?.focus()
  }, 0)
}

watch(open, async (isOpen) => {
  if (!isOpen) return
  mode.value = props.activityId ? 'edit' : 'create'
  reset()
  if (props.activityId) {
    await loadDetail()
    if (!open.value) return // fetch failed, dialog already closed
  }
  await nextTick()
  focusActivityType()
})

// If the dialog was opened while activity types were still loading,
// the select is disabled and focus() is a no-op — focus it once loaded.
watch(activityTypesStatus, async (status) => {
  if (status !== 'success' || !open.value) return
  await nextTick()
  focusActivityType()
})

function cancel() {
  open.value = false
}

async function onSubmit(event: FormSubmitEvent<Schema>) {
  if (submitting.value) return
  submitting.value = true
  try {
    const result = await upsertGeneralSchedule({
      body: {
        id: isEditMode.value ? props.activityId : null,
        schedule_activity_type_id: event.data.scheduleActivityTypeId,
        name: event.data.name,
        start_at: `${event.data.date}T${event.data.startTime}`,
        end_at: event.data.endTime ? `${event.data.date}T${event.data.endTime}` : null,
        detail: isEditMode.value ? editDetail.value : null,
        is_attendence_check: event.data.isAttendenceCheck
      }
    })

    const saved = result
    const activityType = activityTypes.value.find(
      option => option.id === saved.schedule_activity_type_id
    )
    const activity: ScheduleActivity = {
      id: saved.id,
      color: activityType?.color ?? '#6b7280',
      name: saved.name,
      startAt: saved.start_at,
      endAt: saved.end_at ?? undefined,
      isAttendenceCheck: saved.is_attendence_check
    }
    if (isEditMode.value) {
      emit('update', activity)
    } else {
      emit('create', activity)
    }
    toast.add({
      title: isEditMode.value
        ? t('studyYearSchedules.addDay.updateSuccess')
        : t('studyYearSchedules.addDay.createSuccess'),
      color: 'success'
    })
    open.value = false
  } catch {
    toast.add({
      title: isEditMode.value
        ? t('studyYearSchedules.addDay.updateFailed')
        : t('studyYearSchedules.addDay.createFailed'),
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
    :title="isEditMode ? t('studyYearSchedules.addDay.editTitle') : t('studyYearSchedules.addDay.title')"
    :dismissible="!submitting && !loadingDetail"
  >
    <UButton
      :label="t('studyYearSchedules.addDay.title')"
      icon="i-lucide-plus"
    />

    <template #body>
      <!-- Edit mode: detail fetched via API — placeholder the form layout while loading -->
      <div
        v-if="loadingDetail"
        class="space-y-4"
        aria-busy="true"
      >
        <div class="space-y-2">
          <USkeleton class="h-4 w-28" />
          <USkeleton class="h-9 w-full" />
        </div>
        <div class="flex items-end gap-4">
          <div class="min-w-0 flex-1 space-y-2">
            <USkeleton class="h-4 w-16" />
            <USkeleton class="h-9 w-full" />
          </div>
          <USkeleton class="mb-1.5 h-6 w-24" />
        </div>
        <div class="space-y-2">
          <USkeleton class="h-4 w-12" />
          <USkeleton class="h-9 w-full" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <USkeleton class="h-4 w-24" />
            <USkeleton class="h-9 w-full" />
          </div>
          <div class="space-y-2">
            <USkeleton class="h-4 w-24" />
            <USkeleton class="h-9 w-full" />
          </div>
        </div>
        <div class="flex justify-end gap-2">
          <USkeleton class="h-9 w-16" />
          <USkeleton class="h-9 w-20" />
        </div>
      </div>

      <UForm
        v-else
        :schema="schema"
        :state="state"
        :disabled="submitting || loadingDetail"
        class="space-y-4"
        @submit="onSubmit"
      >
        <UFormField
          :label="t('studyYearSchedules.addDay.activityType')"
          name="scheduleActivityTypeId"
          required
        >
          <USelectMenu
            ref="activityTypeSelect"
            v-model="state.scheduleActivityTypeId"
            :items="activityTypes"
            value-key="id"
            :placeholder="t('studyYearSchedules.addDay.activityTypePlaceholder')"
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
          <span>{{ t('studyYearSchedules.addDay.activityTypeLoadError') }}</span>
          <UButton
            :label="t('studyYearSchedules.addDay.retry')"
            color="error"
            variant="soft"
            size="xs"
            @click="loadActivityTypes"
          />
        </div>

        <div class="flex items-end gap-4">
          <UFormField
            :label="t('studyYearSchedules.addDay.name')"
            name="name"
            required
            class="min-w-0 flex-1"
          >
            <UInput
              v-model="state.name"
              :placeholder="t('studyYearSchedules.addDay.namePlaceholder')"
              maxlength="100"
              class="w-full"
            />
          </UFormField>
          <UFormField
            name="isAttendenceCheck"
            class="pb-1.5"
          >
            <UCheckbox
              v-model="state.isAttendenceCheck"
              :label="t('studyYearSchedules.addDay.attendance')"
              :disabled="submitting"
            />
          </UFormField>
        </div>

        <UFormField
          :label="t('studyYearSchedules.addDay.date')"
          name="date"
          required
        >
          <UPopover :content="{ align: 'start' }">
            <UButton
              type="button"
              color="neutral"
              variant="outline"
              trailing-icon="i-lucide-calendar"
              :label="displayDate"
              :class="!state.date && 'text-dimmed'"
              :disabled="submitting"
              class="w-full justify-between"
            />
            <template #content>
              <UCalendar
                v-model="selectedDate"
                locale="vi"
              />
            </template>
          </UPopover>
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField
            :label="t('studyYearSchedules.addDay.startTime')"
            name="startTime"
            required
          >
            <CommonTimePicker
              v-model="state.startTime"
              :disabled="submitting"
            />
          </UFormField>
          <UFormField
            :label="t('studyYearSchedules.addDay.endTime')"
            name="endTime"
          >
            <CommonTimePicker
              v-model="state.endTime"
              :disabled="submitting"
              clearable
            />
          </UFormField>
        </div>

        <div class="flex justify-end gap-2">
          <UButton
            :label="t('studyYearSchedules.addDay.cancel')"
            type="button"
            color="neutral"
            variant="subtle"
            :disabled="submitting"
            @click="cancel"
          />
          <UButton
            :label="isEditMode ? t('studyYearSchedules.addDay.update') : t('studyYearSchedules.addDay.create')"
            type="submit"
            color="primary"
            :loading="submitting"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
