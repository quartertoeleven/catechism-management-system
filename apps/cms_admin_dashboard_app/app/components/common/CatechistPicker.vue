<script setup lang="ts">
import { listCatechists, type CatechistSchema } from '~/generated-client'

const { t } = useI18n()
const toast = useToast()

const model = defineModel<string | null>({ default: null })

const props = defineProps<{
  placeholder?: string
  disabled?: boolean
  selectedCatechist?: CatechistSchema | null
}>()

interface PickerItem {
  label: string
  value: string
}

const items = ref<PickerItem[]>([])
const loading = ref(false)
const failed = ref(false)
const searchTerm = ref('')

const SEARCH_DEBOUNCE_MS = 250
const MIN_SEARCH_LENGTH = 2

let requestSeq = 0
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function toItem(catechist: CatechistSchema): PickerItem {
  const name = [catechist.first_name, catechist.middle_name, catechist.last_name]
    .filter(Boolean)
    .join(' ')
  return {
    label: name ? `${name} (${catechist.code})` : catechist.code,
    value: catechist.id
  }
}

async function fetchItems(term: string) {
  if (term.length < MIN_SEARCH_LENGTH) {
    requestSeq += 1 // invalidate any in-flight request
    items.value = []
    loading.value = false
    return
  }
  const seq = ++requestSeq
  loading.value = true
  try {
    const result = await listCatechists({ query: { query: term || undefined } })
    if (seq !== requestSeq) return // stale response superseded by a newer request
    const fetched = (result.data ?? []).map(toItem)
    // Keep the selected item's label visible when search filters it out.
    const selected = model.value
      ? items.value.find(item => item.value === model.value)
      : undefined
    items.value = selected && !fetched.some(item => item.value === selected.value)
      ? [selected, ...fetched]
      : fetched
    failed.value = false
  } catch {
    if (seq !== requestSeq) return
    if (!failed.value) {
      toast.add({
        title: t('common.catechistPicker.loadError'),
        color: 'error'
      })
    }
    failed.value = true // keep showing the last good list
  } finally {
    if (seq === requestSeq) loading.value = false
  }
}

function onOpenChange(isOpen: boolean) {
  if (!isOpen) return
  // Refresh on every open — a previous session may hold a stale filtered
  // list. Below the minimum length the guard clears the list instead.
  fetchItems(searchTerm.value)
}

function onSearchTerm(term: string) {
  searchTerm.value = term
  if (debounceTimer) {
    clearTimeout(debounceTimer)
    debounceTimer = null
  }
  if (term.length < MIN_SEARCH_LENGTH) {
    fetchItems(term) // clear immediately, no debounce
    return
  }
  debounceTimer = setTimeout(() => fetchItems(term), SEARCH_DEBOUNCE_MS)
}

/** Load the label for a pre-selected id so a raw id is never displayed. */
async function hydrateSelectedLabel(id: string) {
  try {
    const result = await listCatechists({ query: { ids: [id] } })
    if (model.value !== id) return // selection changed while in flight
    const catechist = result.data?.[0]
    if (!catechist) return
    const item = toItem(catechist)
    if (!items.value.some(existing => existing.value === item.value)) {
      items.value = [...items.value, item]
    }
  } catch {
    if (!failed.value) {
      toast.add({
        title: t('common.catechistPicker.loadError'),
        color: 'error'
      })
    }
    failed.value = true
  }
}

// Edit mode supplies the whole catechist — seed its label without an API call.
watch(() => props.selectedCatechist, (value) => {
  if (!value || model.value !== value.id) return
  if (items.value.some(item => item.value === value.id)) return
  items.value = [...items.value, toItem(value)]
}, { immediate: true })

// Prefills the model with a bare id — fetch its label (fallback).
watch(model, (value) => {
  if (!value) return
  if (items.value.some(item => item.value === value)) return
  void hydrateSelectedLabel(value)
}, { immediate: true })

onUnmounted(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
})
</script>

<template>
  <USelectMenu
    v-model="model"
    :items="items"
    value-key="value"
    :placeholder="placeholder ?? t('common.catechistPicker.placeholder')"
    :search-input="{ placeholder: t('common.catechistPicker.searchPlaceholder') }"
    :loading="loading"
    :disabled="disabled"
    :ignore-filter="true"
    :reset-search-term-on-blur="false"
    :reset-search-term-on-select="false"
    clear
    class="w-full"
    @update:search-term="onSearchTerm"
    @update:open="onOpenChange"
  >
    <template #empty="{ searchTerm: term }">
      <p
        v-if="term.length < MIN_SEARCH_LENGTH"
        class="text-sm"
      >
        {{ t('common.catechistPicker.minChars') }}
      </p>
      <p
        v-else
        class="text-sm"
      >
        {{ t('common.catechistPicker.noResults') }}
      </p>
    </template>
  </USelectMenu>
</template>
