<script setup lang="ts">
const { t } = useI18n()

const props = defineProps<{ disabled?: boolean, clearable?: boolean }>()

const modelValue = defineModel<string | undefined>({ default: undefined })

const open = ref(false)

const HOURS = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'))
const MINUTES = ['00', '10', '20', '30', '40', '50']

const selectedHour = computed(() => (modelValue.value ? modelValue.value.slice(0, 2) : undefined))
const selectedMinute = computed(() => (modelValue.value ? modelValue.value.slice(3, 5) : undefined))

const label = computed(() => modelValue.value || t('studyYearSchedules.addDay.timePlaceholder'))

function pickHour(hour: string) {
  modelValue.value = `${hour}:${selectedMinute.value ?? '00'}`
}

function pickMinute(minute: string) {
  if (!selectedHour.value) return
  modelValue.value = `${selectedHour.value}:${minute}`
  open.value = false
}

function clear() {
  modelValue.value = undefined
  open.value = false
}
</script>

<template>
  <UPopover v-model:open="open" :content="{ align: 'start' }">
    <div class="relative w-full">
      <UButton
        type="button"
        color="neutral"
        variant="outline"
        trailing-icon="i-lucide-clock"
        :label="label"
        :class="!modelValue && 'text-dimmed'"
        :disabled="props.disabled"
        :ui="{ trailingIcon: props.clearable && modelValue ? 'mr-5' : undefined }"
        class="w-full justify-between"
      />
      <UButton
        v-if="props.clearable && modelValue"
        icon="i-lucide-x"
        color="neutral"
        variant="ghost"
        size="xs"
        :disabled="props.disabled"
        :aria-label="t('studyYearSchedules.addDay.clearTime')"
        class="absolute top-1/2 right-1 -translate-y-1/2"
        @click.stop="clear"
      />
    </div>

    <template #content>
      <div class="flex gap-1 p-1">
        <div class="flex w-12 flex-col">
          <span class="px-2 pb-1 text-center text-xs font-medium text-dimmed">{{ t('studyYearSchedules.addDay.hoursColumn') }}</span>
          <div class="max-h-60 overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            <button
              v-for="hour in HOURS"
              :key="hour"
              type="button"
              :class="[
                'mx-auto block w-10 rounded px-2 py-1.5 text-center text-sm hover:bg-elevated/50',
                hour === selectedHour ? 'bg-elevated font-semibold text-highlighted' : 'text-default'
              ]"
              @click="pickHour(hour)"
            >
              {{ hour }}
            </button>
          </div>
        </div>
        <div class="flex w-12 flex-col">
          <span class="px-2 pb-1 text-center text-xs font-medium text-dimmed">{{ t('studyYearSchedules.addDay.minutesColumn') }}</span>
          <div class="max-h-60 overflow-y-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            <button
              v-for="minute in MINUTES"
              :key="minute"
              type="button"
              :disabled="!modelValue"
              :class="[
                'mx-auto block w-10 rounded px-2 py-1.5 text-center text-sm hover:bg-elevated/50',
                minute === selectedMinute ? 'bg-elevated font-semibold text-highlighted' : 'text-default',
                !modelValue && 'cursor-not-allowed opacity-50 hover:bg-transparent'
              ]"
              @click="pickMinute(minute)"
            >
              {{ minute }}
            </button>
          </div>
        </div>
      </div>
    </template>
  </UPopover>
</template>
