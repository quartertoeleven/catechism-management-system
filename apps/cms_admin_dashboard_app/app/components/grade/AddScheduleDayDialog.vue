<script setup lang="ts">
import * as z from 'zod'
import { CalendarDate } from '@internationalized/date'
import type { FormSubmitEvent } from '@nuxt/ui'
import {
  getGradeSchedule,
  listGeneralSchedules,
  listScheduleActivityTypes,
  upsertGradeSchedule,
  type GeneralScheduleListItem
} from '~/generated-client'
import type { GradeScheduleActivity } from '~/types'

const { t } = useI18n()
const toast = useToast()

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{
  activityId?: string | null
  duplicate?: boolean
  gradeId: string
}>()

const emit = defineEmits<{
  create: [activity: GradeScheduleActivity]
  update: [activity: GradeScheduleActivity]
}>()

// Frozen at open time — recomputing from `activityId` while the modal is
// still fading out would flip the title/buttons back to create mode.
// `duplicate` fetches the source record like edit, but submits an insert.
const mode = ref<'create' | 'edit' | 'duplicate'>('create')
const isEditMode = computed(() => mode.value === 'edit')

const dialogTitle = computed(() => {
  if (mode.value === 'edit') return t('gradeSchedules.addDay.editTitle')
  if (mode.value === 'duplicate') return t('gradeSchedules.addDay.duplicateTitle')
  return t('gradeSchedules.addDay.title')
})

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

/** A general schedule activity the form can be prefilled from. */
interface GeneralScheduleOption {
  id: string
  label: string
  color: string
  source: GeneralScheduleListItem
}

const generalSchedules = ref<GeneralScheduleOption[]>([])
const generalSchedulesStatus = ref<'pending' | 'success' | 'error'>('pending')

function mapGeneralScheduleOption(item: GeneralScheduleListItem): GeneralScheduleOption {
  return {
    id: item.id,
    label: `${item.name} — ${item.start_at.slice(0, 10)} ${item.start_at.slice(11, 16)}`,
    color: toCssColor(item.schedule_activity_type_color),
    source: item
  }
}

async function loadGeneralSchedules() {
  generalSchedulesStatus.value = 'pending'
  try {
    const result = await listGeneralSchedules({})
    generalSchedules.value = (result.data ?? []).map(mapGeneralScheduleOption)
    generalSchedulesStatus.value = 'success'
  } catch {
    generalSchedulesStatus.value = 'error'
  }
}

onMounted(() => {
  loadActivityTypes()
  loadGeneralSchedules()
})

const schema = z.object({
  generalScheduleId: z.string().nullable(),
  scheduleActivityTypeId: z.number(t('gradeSchedules.addDay.validation.activityTypeRequired')),
  name: z.string()
    .min(1, t('gradeSchedules.addDay.validation.nameRequired'))
    .max(100, t('gradeSchedules.addDay.validation.nameMax')),
  isAttendenceCheck: z.boolean(),
  date: z.string().min(1, t('gradeSchedules.addDay.validation.dateRequired')),
  startTime: z.string().min(1, t('gradeSchedules.addDay.validation.startTimeRequired')),
  endTime: z.string().optional()
}).superRefine((value, ctx) => {
  if (value.endTime && value.endTime <= value.startTime) {
    ctx.addIssue({
      code: 'custom',
      path: ['endTime'],
      message: t('gradeSchedules.addDay.validation.endTimeAfterStartTime')
    })
  }
})

type Schema = z.output<typeof schema>

const state = reactive<Partial<Schema>>({
  generalScheduleId: null,
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

const selectedGeneralScheduleId = computed<string | undefined>({
  get: () => state.generalScheduleId ?? undefined,
  set: (value) => {
    state.generalScheduleId = value ?? null
    const option = generalSchedules.value.find(item => item.id === value)
    if (option) prefillFromGeneralSchedule(option.source)
  }
})

/** Overwrite every editable field with the chosen general schedule's values. */
function prefillFromGeneralSchedule(item: GeneralScheduleListItem) {
  state.scheduleActivityTypeId = item.schedule_activity_type_id
  state.name = item.name
  state.date = item.start_at.slice(0, 10)
  state.startTime = item.start_at.slice(11, 16)
  state.endTime = item.end_at ? item.end_at.slice(11, 16) : undefined
  state.isAttendenceCheck = item.is_attendence_check
  editDetail.value = item.detail
}

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
  if (!state.date) return t('gradeSchedules.addDay.datePlaceholder')
  const [year, month, day] = state.date.split('-')
  return `${day}/${month}/${year}`
})

function reset() {
  state.generalScheduleId = null
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
    const result = await getGradeSchedule({
      path: { schedule_id: props.activityId }
    })
    state.generalScheduleId = result.general_schedule_id
    state.scheduleActivityTypeId = result.schedule_activity_type_id
    state.name = result.name
    state.date = result.start_at.slice(0, 10)
    state.startTime = result.start_at.slice(11, 16)
    state.endTime = result.end_at ? result.end_at.slice(11, 16) : undefined
    state.isAttendenceCheck = result.is_attendence_check
    editDetail.value = result.detail
  } catch {
    toast.add({
      title: t('gradeSchedules.loadError'),
      color: 'error'
    })
    open.value = false
  } finally {
    loadingDetail.value = false
  }
}

/** Append " (bản sao)" keeping the result within the 100-char name limit. */
function withDuplicateSuffix(name: string) {
  const suffix = ` ${t('gradeSchedules.addDay.duplicateSuffix')}`
  if (name.length + suffix.length <= 100) return name + suffix
  return `${name.slice(0, 100 - suffix.length)}${suffix}`
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
  mode.value = props.activityId
    ? (props.duplicate ? 'duplicate' : 'edit')
    : 'create'
  reset()
  if (props.activityId) {
    await loadDetail()
    if (!open.value) return // fetch failed, dialog already closed
    if (mode.value === 'duplicate') {
      state.name = withDuplicateSuffix(state.name ?? '')
    }
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
    const result = await upsertGradeSchedule({
      body: {
        // Duplicate fetched the source record but must insert a new row.
        id: mode.value === 'edit' ? props.activityId : null,
        grade_id: props.gradeId,
        general_schedule_id: event.data.generalScheduleId,
        schedule_activity_type_id: event.data.scheduleActivityTypeId,
        name: event.data.name,
        start_at: `${event.data.date}T${event.data.startTime}`,
        end_at: event.data.endTime ? `${event.data.date}T${event.data.endTime}` : null,
        detail: mode.value === 'create' ? null : editDetail.value,
        is_attendence_check: event.data.isAttendenceCheck
      }
    })

    const saved = result
    const activityType = activityTypes.value.find(
      option => option.id === saved.schedule_activity_type_id
    )
    const activity: GradeScheduleActivity = {
      id: saved.id,
      generalScheduleId: saved.general_schedule_id,
      color: activityType?.color ?? '#6b7280',
      activityTypeName: activityType?.label ?? '',
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
        ? t('gradeSchedules.addDay.updateSuccess')
        : t('gradeSchedules.addDay.createSuccess'),
      color: 'success'
    })
    open.value = false
  } catch {
    toast.add({
      title: isEditMode.value
        ? t('gradeSchedules.addDay.updateFailed')
        : t('gradeSchedules.addDay.createFailed'),
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
    :title="dialogTitle"
    :dismissible="!submitting && !loadingDetail"
  >
    <template #body>
      <!-- Edit mode: detail fetched via API — placeholder the form layout while loading -->
      <div
        v-if="loadingDetail"
        class="space-y-4"
        aria-busy="true"
      >
        <div class="space-y-2">
          <USkeleton class="h-4 w-32" />
          <USkeleton class="h-9 w-full" />
        </div>
        <div class="space-y-2">
          <USkeleton class="h-4 w-28" />
          <USkeleton class="h-9 w-full" />
        </div>
        <div class="flex items-end gap-4">
          <div class="min-w-0 flex-1 space-y-2">
            <USkeleton class="h-4 w-16" />
            <USkeleton class="h-9 w-full" />
          </div>
          <div class="mb-1.5">
            <USkeleton class="h-6 w-24" />
          </div>
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
          :label="t('gradeSchedules.addDay.generalSchedule')"
          name="generalScheduleId"
        >
          <USelectMenu
            v-model="selectedGeneralScheduleId"
            :items="generalSchedules"
            value-key="id"
            clearable
            :placeholder="t('gradeSchedules.addDay.generalSchedulePlaceholder')"
            :loading="generalSchedulesStatus === 'pending'"
            :disabled="generalSchedulesStatus !== 'success'"
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
          v-if="generalSchedulesStatus === 'error'"
          class="flex items-center gap-2 text-sm text-error"
        >
          <span>{{ t('gradeSchedules.addDay.generalScheduleLoadError') }}</span>
          <UButton
            :label="t('gradeSchedules.addDay.retry')"
            color="error"
            variant="soft"
            size="xs"
            @click="loadGeneralSchedules"
          />
        </div>

        <UFormField
          :label="t('gradeSchedules.addDay.activityType')"
          name="scheduleActivityTypeId"
          required
        >
          <USelectMenu
            ref="activityTypeSelect"
            v-model="state.scheduleActivityTypeId"
            :items="activityTypes"
            value-key="id"
            :placeholder="t('gradeSchedules.addDay.activityTypePlaceholder')"
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
          <span>{{ t('gradeSchedules.addDay.activityTypeLoadError') }}</span>
          <UButton
            :label="t('gradeSchedules.addDay.retry')"
            color="error"
            variant="soft"
            size="xs"
            @click="loadActivityTypes"
          />
        </div>

        <div class="flex items-end gap-4">
          <UFormField
            :label="t('gradeSchedules.addDay.name')"
            name="name"
            required
            class="min-w-0 flex-1"
          >
            <UInput
              v-model="state.name"
              :placeholder="t('gradeSchedules.addDay.namePlaceholder')"
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
              :label="t('gradeSchedules.addDay.attendance')"
              :disabled="submitting"
            />
          </UFormField>
        </div>

        <UFormField
          :label="t('gradeSchedules.addDay.date')"
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
            :label="t('gradeSchedules.addDay.startTime')"
            name="startTime"
            required
          >
            <CommonTimePicker
              v-model="state.startTime"
              :disabled="submitting"
            />
          </UFormField>
          <UFormField
            :label="t('gradeSchedules.addDay.endTime')"
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
            :label="t('gradeSchedules.addDay.cancel')"
            type="button"
            color="neutral"
            variant="subtle"
            :disabled="submitting"
            @click="cancel"
          />
          <UButton
            :label="isEditMode ? t('gradeSchedules.addDay.update') : t('gradeSchedules.addDay.create')"
            type="submit"
            color="primary"
            :loading="submitting"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
