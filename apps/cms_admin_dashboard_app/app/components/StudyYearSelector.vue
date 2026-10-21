<script setup lang="ts">
import type { DropdownMenuItem } from '@nuxt/ui'
import {
  listStudyYears,
  type StudyYearInfo,
  type StudyYearListItem
} from '~/generated-client'

defineProps<{
  collapsed?: boolean
}>()

const studyYears = ref<StudyYearListItem[]>([])
const selected = ref<StudyYearListItem | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const result = await listStudyYears({})
    studyYears.value = result.data ?? []
  } catch {
    studyYears.value = []
  } finally {
    loading.value = false
  }

  const stored = getAppState<StudyYearInfo>('current_selected_study_year')
  selected.value = studyYears.value.find(year => year.id === stored?.id)
    ?? studyYears.value.find(year => year.is_current)
    ?? studyYears.value[0]
    ?? null
})

const items = computed<DropdownMenuItem[][]>(() => [
  studyYears.value.map(year => ({
    label: year.name,
    description: year.code,
    onSelect() {
      selected.value = year
      setAppState('current_selected_study_year', {
        id: year.id,
        code: year.code,
        name: year.name
      })
    }
  }))
])
</script>

<template>
  <USkeleton
    v-if="loading"
    aria-busy="true"
    :class="collapsed ? 'h-10 w-10 shrink-0' : 'h-10 w-full'"
  />

  <UDropdownMenu
    v-else
    :items="items"
    :content="{ align: 'center', collisionPadding: 12 }"
    :ui="{ content: collapsed ? 'w-40' : 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton
      v-bind="{
        label: collapsed ? undefined : selected?.name,
        icon: collapsed ? 'i-lucide-school' : undefined,
        trailingIcon: collapsed ? undefined : 'i-lucide-chevrons-up-down'
      }"
      color="neutral"
      variant="ghost"
      block
      :square="collapsed"
      :disabled="!selected"
      class="data-[state=open]:bg-elevated"
      :class="[!collapsed && 'py-2']"
      :ui="{
        trailingIcon: 'text-dimmed'
      }"
    />
  </UDropdownMenu>
</template>
