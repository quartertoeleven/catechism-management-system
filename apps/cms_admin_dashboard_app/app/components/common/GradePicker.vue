<script setup lang="ts">
import type { GradeListItem, StudyYearInfo } from '~/generated-client'
import { listGrades } from '~/generated-client'

const { t } = useI18n()

defineProps<{
  /** Show "Khối đang chọn:" (bold + muted) as part of the picker's display value. */
  labelInValue?: boolean
}>()

const selected = defineModel<GradeListItem | null>('selected', { default: null })

const grades = ref<GradeListItem[]>([])
const loading = ref(true)
const loadError = ref(false)

const SELECTED_GRADE_KEY = 'current_selected_grade'

async function loadGrades() {
  loading.value = true
  loadError.value = false
  try {
    // Follow the study year chosen in the sidebar selector, if any.
    const studyYear = getAppState<StudyYearInfo>('current_selected_study_year')
    const result = await listGrades(
      studyYear?.code ? { query: { study_year_code: studyYear.code } } : {}
    )
    grades.value = result.data ?? []
    const stored = getAppState<{ id: string }>(SELECTED_GRADE_KEY)
    const initial = grades.value.find(grade => grade.id === stored?.id)
      ?? grades.value[0]
      ?? null
    selected.value = initial
    // NOTE: pass the value explicitly — `selected.value` reads the v-model
    // prop, which is still stale synchronously after assignment.
    persistSelection(initial)
  } catch {
    loadError.value = true
    grades.value = []
    selected.value = null
  } finally {
    loading.value = false
  }
}

function onSelect(gradeId: string) {
  const grade = grades.value.find(item => item.id === gradeId) ?? null
  selected.value = grade
  persistSelection(grade)
}

function persistSelection(grade: GradeListItem | null) {
  if (grade) {
    setAppState(SELECTED_GRADE_KEY, {
      id: grade.id,
      code: grade.code,
      name: grade.name
    })
  }
}

onMounted(loadGrades)
</script>

<template>
  <div class="flex items-center gap-2">
    <USkeleton
      v-if="loading"
      class="h-9 w-40 shrink-0"
      aria-busy="true"
    />

    <template v-else-if="loadError">
      <span class="text-sm text-error">{{ t('gradeSchedules.selector.loadError') }}</span>
      <UButton
        :label="t('gradeSchedules.selector.retry')"
        color="error"
        variant="soft"
        size="xs"
        @click="loadGrades"
      />
    </template>

    <USelectMenu
      v-else
      :model-value="selected?.id"
      :items="grades"
      value-key="id"
      label-key="name"
      :placeholder="t('gradeSchedules.selector.placeholder')"
      class="w-56"
      :ui="{ itemLabel: 'font-medium' }"
      @update:model-value="onSelect"
    >
      <template #default>
        <span
          v-if="labelInValue"
          class="font-semibold text-muted"
        >{{ t('gradeSchedules.selector.label') }}</span>
        <span
          v-if="selected"
          data-slot="value"
        >{{ selected.name }}</span>
        <span
          v-else
          data-slot="placeholder"
          class="text-dimmed"
        >{{ t('gradeSchedules.selector.placeholder') }}</span>
      </template>

      <template #item="{ item }">
        <div class="flex items-baseline gap-2">
          <span class="truncate">{{ item.name }}</span>
          <span class="truncate text-xs text-dimmed">{{ item.code }}</span>
        </div>
      </template>
    </USelectMenu>
  </div>
</template>
