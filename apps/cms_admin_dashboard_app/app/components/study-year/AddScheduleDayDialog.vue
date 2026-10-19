<script setup lang="ts">
import * as z from 'zod'
import { CalendarDate } from '@internationalized/date'
import type { FormSubmitEvent } from '@nuxt/ui'
import { listScheduleActivityTypes } from '~/generated-client'
import type { ScheduleActivity } from '~/types'

const { t } = useI18n()
const toast = useToast()

const open = ref(false)

const emit = defineEmits<{
  create: [activity: ScheduleActivity]
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
      color: item.color ?? '#6b7280'
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
  date: '',
  startTime: '',
  endTime: undefined
})

const submitting = ref(false)

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
  reset()
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
    const payload = {
      scheduleActivityTypeId: event.data.scheduleActivityTypeId,
      name: event.data.name,
      startAt: `${event.data.date}T${event.data.startTime}`,
      endAt: event.data.endTime ? `${event.data.date}T${event.data.endTime}` : undefined
    }
    console.log('Create schedule day — payload for backend:', payload)

    await new Promise(resolve => setTimeout(resolve, 3000))
    const activityType = activityTypes.value.find(option => option.id === payload.scheduleActivityTypeId)
    emit('create', {
      color: activityType?.color ?? '#6b7280',
      name: payload.name,
      startAt: payload.startAt,
      endAt: payload.endAt
    })
    toast.add({
      title: t('studyYearSchedules.addDay.createSuccess'),
      color: 'success'
    })
    open.value = false
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <UModal
    v-model:open="open"
    :title="t('studyYearSchedules.addDay.title')"
    :dismissible="!submitting"
  >
    <UButton
      :label="t('studyYearSchedules.addDay.title')"
      icon="i-lucide-plus"
    />

    <template #body>
      <UForm
        :schema="schema"
        :state="state"
        :disabled="submitting"
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
              <span
                class="h-2 w-2 shrink-0 rounded-full"
                :style="{ backgroundColor: item.color }"
              />
              <span>{{ item.label }}</span>
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

        <UFormField
          :label="t('studyYearSchedules.addDay.name')"
          name="name"
          required
        >
          <UInput
            v-model="state.name"
            :placeholder="t('studyYearSchedules.addDay.namePlaceholder')"
            maxlength="100"
            class="w-full"
          />
        </UFormField>

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
            :label="t('studyYearSchedules.addDay.create')"
            type="submit"
            color="primary"
            :loading="submitting"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
