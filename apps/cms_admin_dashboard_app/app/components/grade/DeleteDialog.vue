<script setup lang="ts">
import { deleteGrade, type GradeListItem } from '~/generated-client'

const { t } = useI18n()
const toast = useToast()

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{ grade: GradeListItem | null }>()

const emit = defineEmits<{
  delete: [gradeId: string]
}>()

const submitting = ref(false)

async function onDelete() {
  if (submitting.value || !props.grade) return
  submitting.value = true
  try {
    await deleteGrade({ path: { grade_id: props.grade.id } })
    emit('delete', props.grade.id)
    toast.add({
      title: t('studyYearGrades.actions.deleteSuccess'),
      color: 'success'
    })
    open.value = false
  } catch (error) {
    // ofetch surfaces the FastAPI error body on `data` for non-2xx responses.
    const data = (error as { data?: { detail?: unknown } })?.data
    const detail = typeof data?.detail === 'string' ? data.detail : undefined
    toast.add({
      title: detail ?? t('studyYearGrades.actions.deleteFailed'),
      color: 'error'
    })
    // Dialog stays open on failure.
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <UModal
    v-model:open="open"
    :title="t('studyYearGrades.actions.deleteConfirmTitle')"
    :dismissible="!submitting"
    :ui="{ footer: 'justify-end' }"
  >
    <template #body>
      <p class="text-sm text-muted">
        {{ t('studyYearGrades.actions.deleteConfirmDescription') }}
      </p>

      <div
        v-if="grade"
        class="mt-3 space-y-1.5 rounded-lg bg-elevated/50 p-3 text-sm"
      >
        <div class="flex gap-2">
          <span class="w-28 shrink-0 text-muted">{{ t('studyYearGrades.columns.code') }}</span>
          <span class="min-w-0 font-medium text-highlighted">{{ grade.code }}</span>
        </div>
        <div class="flex gap-2">
          <span class="w-28 shrink-0 text-muted">{{ t('studyYearGrades.columns.name') }}</span>
          <span class="min-w-0 font-medium text-highlighted">{{ grade.name }}</span>
        </div>
      </div>
    </template>

    <template #footer>
      <UButton
        :label="t('studyYearGrades.add.cancel')"
        color="neutral"
        variant="subtle"
        :disabled="submitting"
        @click="open = false"
      />
      <UButton
        :label="t('studyYearGrades.actions.delete')"
        icon="i-lucide-trash-2"
        color="error"
        :loading="submitting"
        @click="onDelete"
      />
    </template>
  </UModal>
</template>
