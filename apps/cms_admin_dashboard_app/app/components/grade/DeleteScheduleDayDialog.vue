<script setup lang="ts">
import { deleteGradeSchedule } from '~/generated-client'
import type { GradeScheduleActivity } from '~/types'

const { t } = useI18n()
const toast = useToast()

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{ activity?: GradeScheduleActivity | null }>()

const emit = defineEmits<{
  delete: [activity: GradeScheduleActivity]
}>()

const deleting = ref(false)

function formatDate(isoDateTime: string) {
  const [year, month, day] = isoDateTime.slice(0, 10).split('-')
  return `${day}/${month}/${year}`
}

async function onConfirm() {
  if (!props.activity || deleting.value) return
  deleting.value = true
  try {
    await deleteGradeSchedule({
      path: { schedule_id: props.activity.id }
    })
    emit('delete', props.activity)
    toast.add({
      title: t('gradeSchedules.deleteDay.deleteSuccess'),
      color: 'success'
    })
    open.value = false
  } catch {
    toast.add({
      title: t('gradeSchedules.deleteDay.deleteFailed'),
      color: 'error'
    })
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <UModal
    v-model:open="open"
    :title="t('gradeSchedules.deleteDay.title')"
    :dismissible="!deleting"
    :ui="{ footer: 'justify-end' }"
  >
    <template #body>
      <p class="text-sm text-muted">
        {{ t('gradeSchedules.deleteDay.confirmText') }}
      </p>

      <div
        v-if="activity"
        class="mt-3 space-y-1.5 rounded-lg bg-elevated/50 p-3 text-sm"
      >
        <div class="flex gap-2">
          <span class="w-28 shrink-0 text-muted">{{ t('gradeSchedules.addDay.activityType') }}</span>
          <span class="min-w-0 font-medium text-highlighted">{{ activity.activityTypeName }}</span>
        </div>
        <div class="flex gap-2">
          <span class="w-28 shrink-0 text-muted">{{ t('gradeSchedules.addDay.name') }}</span>
          <span class="min-w-0 font-medium text-highlighted">{{ activity.name }}</span>
        </div>
        <div class="flex gap-2">
          <span class="w-28 shrink-0 text-muted">{{ t('gradeSchedules.addDay.date') }}</span>
          <span class="min-w-0 font-medium text-highlighted">{{ formatDate(activity.startAt) }}</span>
        </div>
      </div>
    </template>

    <template #footer>
      <UButton
        :label="t('gradeSchedules.addDay.cancel')"
        color="neutral"
        variant="subtle"
        :disabled="deleting"
        @click="open = false"
      />
      <UButton
        :label="t('gradeSchedules.deleteDay.confirm')"
        icon="i-lucide-trash-2"
        color="error"
        :loading="deleting"
        @click="onConfirm"
      />
    </template>
  </UModal>
</template>
