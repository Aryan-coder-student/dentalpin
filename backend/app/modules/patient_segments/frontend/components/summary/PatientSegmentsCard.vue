<script setup lang="ts">
/**
 * PatientSegmentsCard — clinic-local patient tags (grouping only).
 *
 * Registered into `patient.summary.cards` by patient_segments. Chips of
 * the patient's segments with remove, an add-row (existing segments
 * dropdown + inline create), all gated on `patient_segments.write`.
 */
import type { PatientExtended } from '~~/app/types'
import { PERMISSIONS } from '~~/app/config/permissions'

interface Ctx {
  patient: PatientExtended
}

const props = defineProps<{ ctx: Ctx }>()

const { t } = useI18n()
const { can } = usePermissions()
const canWrite = computed(() => can(PERMISSIONS.patientSegments.write))
const patientId = computed(() => props.ctx.patient.id)
const { segments, allSegments, isLoading, fetchAll, createSegment, assignSegment, removeSegment }
  = usePatientSegments(patientId)

onMounted(fetchAll)

const showAdd = ref(false)
const newName = ref('')

const unassigned = computed(() => {
  const mine = new Set(segments.value.map(s => s.id))
  return allSegments.value.filter(s => !mine.has(s.id))
})

async function addExisting(id: string) {
  await assignSegment(id)
}

async function createAndAssign() {
  const name = newName.value.trim()
  if (!name) return
  await createSegment(name)
  const created = allSegments.value.find(s => s.name === name)
  if (created) await assignSegment(created.id)
  newName.value = ''
  showAdd.value = false
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-2">
      <h3 class="font-semibold">
        {{ t('patientSegments.title') }}
      </h3>
      <UButton
        v-if="canWrite"
        icon="i-lucide-plus"
        size="xs"
        color="neutral"
        variant="ghost"
        :aria-label="t('patientSegments.add')"
        @click="showAdd = !showAdd"
      />
    </div>
    <USkeleton
      v-if="isLoading"
      class="h-6 w-32"
    />
    <p
      v-else-if="segments.length === 0"
      class="text-sm text-muted"
    >
      {{ t('patientSegments.emptyHint') }}
    </p>
    <div
      v-else
      class="flex flex-wrap gap-1.5"
    >
      <UBadge
        v-for="segment in segments"
        :key="segment.id"
        :style="segment.color ? { backgroundColor: segment.color } : {}"
      >
        {{ segment.name }}
        <UButton
          v-if="canWrite"
          icon="i-lucide-x"
          size="xs"
          color="neutral"
          variant="ghost"
          :aria-label="t('patientSegments.remove')"
          @click="removeSegment(segment.id)"
        />
      </UBadge>
    </div>
    <div
      v-if="showAdd && canWrite"
      class="mt-2 space-y-2"
    >
      <USelectMenu
        v-if="unassigned.length > 0"
        :placeholder="t('patientSegments.pickExisting')"
        :items="unassigned.map(s => ({ label: s.name, value: s.id }))"
        @update:model-value="(opt: { value: string }) => addExisting(opt.value)"
      />
      <div class="flex gap-1.5">
        <UInput
          v-model="newName"
          :placeholder="t('patientSegments.newName')"
          class="flex-1"
          @keyup.enter="createAndAssign"
        />
        <UButton
          size="sm"
          @click="createAndAssign"
        >
          {{ t('patientSegments.create') }}
        </UButton>
      </div>
    </div>
  </div>
</template>
