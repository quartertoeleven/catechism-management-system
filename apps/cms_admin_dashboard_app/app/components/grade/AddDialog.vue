<script setup lang="ts">
import * as z from 'zod'
import type { FormSubmitEvent } from '@nuxt/ui'
import {
  createGrade,
  getGrade,
  updateGrade,
  type CatechistSchema,
  type GradeListItem,
  type StudyYearInfo
} from '~/generated-client'

const { t } = useI18n()
const toast = useToast()

const open = defineModel<boolean>('open', { default: false })

const props = defineProps<{ gradeId?: string | null }>()

const emit = defineEmits<{
  create: [grade: GradeListItem]
  update: [grade: GradeListItem]
}>()

const CODE_MAX_LENGTH = 20
const NAME_MAX_LENGTH = 50

const prefix = ref('')
const loadingDetail = ref(false)

// Whole catechist objects from the detail endpoint — the pickers seed
// their labels from these without an extra API call.
const leaderCatechist = ref<CatechistSchema | null>(null)
const viceCatechist = ref<CatechistSchema | null>(null)
const secretaryCatechist = ref<CatechistSchema | null>(null)
const treasurerCatechist = ref<CatechistSchema | null>(null)

// Frozen at open time — mixing create/edit mid-fadeout would flip
// the title/buttons while the modal is still closing.
const mode = ref<'create' | 'edit'>('create')
const isEditMode = computed(() => mode.value === 'edit')

const dialogTitle = computed(() =>
  isEditMode.value
    ? t('studyYearGrades.add.editTitle')
    : t('studyYearGrades.add.title')
)

// Edit mode: fetch the full grade, then prefill the form.
async function loadDetail() {
  if (!props.gradeId) return
  loadingDetail.value = true
  try {
    const detail = await getGrade({ path: { grade_id: props.gradeId } })
    prefix.value = detail.study_year_code
    state.code = detail.code // full code, shown disabled in edit mode
    state.name = detail.name
    state.leader = detail.leader_catechist?.id ?? null
    state.vice = detail.vice_leader_catechist?.id ?? null
    state.secretary = detail.secretary_catechist?.id ?? null
    state.treasurer = detail.treasurer_catechist?.id ?? null
    leaderCatechist.value = detail.leader_catechist
    viceCatechist.value = detail.vice_leader_catechist
    secretaryCatechist.value = detail.secretary_catechist
    treasurerCatechist.value = detail.treasurer_catechist
  } catch {
    toast.add({
      title: t('studyYearGrades.add.loadError'),
      color: 'error'
    })
    open.value = false
  } finally {
    loadingDetail.value = false
  }
}

watch(open, (isOpen) => {
  if (!isOpen) return
  mode.value = props.gradeId ? 'edit' : 'create'
  reset()
  prefix.value = ''
  if (isEditMode.value) {
    void loadDetail()
    return
  }
  // Create mode: the stored study year drives the code prefix.
  // Without a study year there is nothing to prefix with, so never open.
  const stored = getAppState<StudyYearInfo>('current_selected_study_year')
  if (!stored?.code) {
    toast.add({
      title: t('studyYearGrades.add.prefixMissing'),
      color: 'error'
    })
    open.value = false
    return
  }
  prefix.value = stored.code
})

const suffixMax = computed(() => CODE_MAX_LENGTH - prefix.value.length - 1)

const schema = computed(() => z.object({
  // Create mode enforces the suffix rules; edit shows the immutable
  // full code in a disabled input, so no code validation there.
  code: isEditMode.value
    ? z.string()
    : z.string(t('studyYearGrades.add.validation.codeRequired'))
        .trim()
        .min(1, t('studyYearGrades.add.validation.codeRequired'))
        .max(suffixMax.value, t('studyYearGrades.add.validation.codeMax', { max: suffixMax.value }))
        .transform(value => value.toUpperCase()),
  name: z.string()
    .min(1, t('studyYearGrades.add.validation.nameRequired'))
    .max(NAME_MAX_LENGTH, t('studyYearGrades.add.validation.nameMax', { max: NAME_MAX_LENGTH })),
  leader: z.string().nullable().optional(),
  vice: z.string().nullable().optional(),
  secretary: z.string().nullable().optional(),
  treasurer: z.string().nullable().optional()
}))

type Schema = z.output<typeof schema.value>

interface FormState {
  code: string
  name: string
  leader: string | null | undefined
  vice: string | null | undefined
  secretary: string | null | undefined
  treasurer: string | null | undefined
}

const state = reactive<FormState>({
  code: '',
  name: '',
  leader: null,
  vice: null,
  secretary: null,
  treasurer: null
})

const submitting = ref(false)

function reset() {
  state.code = ''
  state.name = ''
  state.leader = null
  state.vice = null
  state.secretary = null
  state.treasurer = null
  leaderCatechist.value = null
  viceCatechist.value = null
  secretaryCatechist.value = null
  treasurerCatechist.value = null
}

function cancel() {
  open.value = false
}

async function onSubmit(event: FormSubmitEvent<Schema>) {
  if (submitting.value) return
  submitting.value = true
  try {
    if (isEditMode.value) {
      if (!props.gradeId) return
      const result = await updateGrade({
        path: { grade_id: props.gradeId },
        body: {
          name: event.data.name,
          leader_catechist_id: event.data.leader ?? null,
          vice_leader_catechist_id: event.data.vice ?? null,
          secretary_catechist_id: event.data.secretary ?? null,
          treasurer_catechist_id: event.data.treasurer ?? null
        }
      })
      emit('update', { id: result.id, code: result.code, name: result.name })
      toast.add({
        title: t('studyYearGrades.add.updateSuccess'),
        color: 'success'
      })
    } else {
      const result = await createGrade({
        body: {
          study_year_code: prefix.value,
          code: event.data.code,
          name: event.data.name,
          leader_catechist_id: event.data.leader ?? null,
          vice_leader_catechist_id: event.data.vice ?? null,
          secretary_catechist_id: event.data.secretary ?? null,
          treasurer_catechist_id: event.data.treasurer ?? null
        }
      })
      emit('create', { id: result.id, code: result.code, name: result.name })
      toast.add({
        title: t('studyYearGrades.add.createSuccess'),
        color: 'success'
      })
    }
    open.value = false
  } catch (error) {
    // ofetch surfaces the FastAPI error body on `data` for non-2xx responses.
    const data = (error as { data?: { detail?: unknown } })?.data
    const detail = typeof data?.detail === 'string' ? data.detail : undefined
    toast.add({
      title: detail ?? (isEditMode.value
        ? t('studyYearGrades.add.updateFailed')
        : t('studyYearGrades.add.createFailed')),
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
    :title="dialogTitle"
    :dismissible="!submitting && !loadingDetail"
  >
    <UButton
      :label="t('studyYearGrades.addGrade')"
      icon="i-lucide-plus"
    />

    <template #body>
      <!-- Skeleton mirrors the form: code, name, catechist grid, buttons -->
      <div
        v-if="loadingDetail"
        class="space-y-4"
        aria-busy="true"
        role="status"
      >
        <div class="space-y-2">
          <USkeleton class="h-4 w-20" />
          <USkeleton class="h-9 w-full" />
        </div>
        <div class="space-y-2">
          <USkeleton class="h-4 w-16" />
          <USkeleton class="h-9 w-full" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div
            v-for="n in 4"
            :key="n"
            class="space-y-2"
          >
            <USkeleton class="h-4 w-24" />
            <USkeleton class="h-9 w-full" />
          </div>
        </div>
        <div class="flex justify-end gap-2">
          <USkeleton class="h-9 w-16" />
          <USkeleton class="h-9 w-24" />
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
          :label="t('studyYearGrades.add.code')"
          name="code"
          required
        >
          <UFieldGroup
            v-if="!isEditMode"
            class="w-full"
          >
            <UInput
              v-model="state.code"
              class="w-full"
              :style="{ '--code-prefix-width': `calc(${prefix.length + 1}ch + 0.5rem)` }"
              :ui="{
                base: 'ps-(--code-prefix-width)',
                leading: 'pointer-events-none'
              }"
              :maxlength="suffixMax"
              :placeholder="t('studyYearGrades.add.codePlaceholder')"
            >
              <template #leading>
                <p class="text-sm text-muted">
                  {{ prefix }}-
                </p>
              </template>
            </UInput>
          </UFieldGroup>
          <UInput
            v-else
            v-model="state.code"
            disabled
            class="w-full"
          />
        </UFormField>

        <UFormField
          :label="t('studyYearGrades.add.name')"
          name="name"
          required
        >
          <UInput
            v-model="state.name"
            class="w-full"
            :maxlength="NAME_MAX_LENGTH"
            :placeholder="t('studyYearGrades.add.namePlaceholder')"
          />
        </UFormField>

        <div class="grid grid-cols-2 gap-4">
          <UFormField
            :label="t('studyYearGrades.add.leader')"
            name="leader"
          >
            <CommonCatechistPicker
              v-model="state.leader"
              :selected-catechist="leaderCatechist"
              :disabled="submitting"
            />
          </UFormField>
          <UFormField
            :label="t('studyYearGrades.add.vice')"
            name="vice"
          >
            <CommonCatechistPicker
              v-model="state.vice"
              :selected-catechist="viceCatechist"
              :disabled="submitting"
            />
          </UFormField>
          <UFormField
            :label="t('studyYearGrades.add.secretary')"
            name="secretary"
          >
            <CommonCatechistPicker
              v-model="state.secretary"
              :selected-catechist="secretaryCatechist"
              :disabled="submitting"
            />
          </UFormField>
          <UFormField
            :label="t('studyYearGrades.add.treasurer')"
            name="treasurer"
          >
            <CommonCatechistPicker
              v-model="state.treasurer"
              :selected-catechist="treasurerCatechist"
              :disabled="submitting"
            />
          </UFormField>
        </div>

        <div class="flex justify-end gap-2">
          <UButton
            :label="t('studyYearGrades.add.cancel')"
            type="button"
            color="neutral"
            variant="subtle"
            :disabled="submitting"
            @click="cancel"
          />
          <UButton
            :label="isEditMode
              ? t('studyYearGrades.add.update')
              : t('studyYearGrades.add.create')"
            type="submit"
            color="primary"
            :loading="submitting"
          />
        </div>
      </UForm>
    </template>
  </UModal>
</template>
