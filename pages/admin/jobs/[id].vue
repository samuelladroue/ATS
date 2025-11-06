<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="mb-4 flex items-center gap-4">
          <NuxtLink
            to="/admin/jobs"
            class="inline-flex items-center text-blue-600 hover:text-blue-700"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Retour aux offres
          </NuxtLink>
          <span class="text-gray-400">|</span>
          <NuxtLink
            to="/"
            class="inline-flex items-center text-blue-600 hover:text-blue-700 text-sm"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            Accueil
          </NuxtLink>
        </div>
        <h1 class="text-3xl font-bold text-gray-900">Candidatures</h1>
        <p class="text-gray-600 mt-1">Job ID: {{ jobId }}</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Chargement des candidatures...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <!-- Kanban board -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <div
          v-for="stage in stages"
          :key="stage.key"
          class="bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <div class="px-4 py-3 border-b border-gray-200 bg-gray-50">
            <h3 class="font-semibold text-gray-900">{{ stage.label }}</h3>
            <p class="text-xs text-gray-500 mt-1">
              {{ getApplicationsByStage(stage.key).length }} candidature(s)
            </p>
          </div>

          <div class="p-3 space-y-2 min-h-[200px]">
            <div
              v-for="app in getApplicationsByStage(stage.key)"
              :key="app.id"
              class="bg-gray-50 rounded-lg p-3 border border-gray-200 hover:shadow-md transition-shadow"
            >
              <div class="mb-2">
                <p class="font-medium text-sm text-gray-900">{{ app.candidate_name }}</p>
                <p class="text-xs text-gray-500">{{ app.candidate_email }}</p>
              </div>

              <div v-if="app.candidate_linkedin_url" class="mb-2">
                <a
                  :href="app.candidate_linkedin_url"
                  target="_blank"
                  rel="noopener"
                  class="text-xs text-blue-600 hover:underline"
                >
                  LinkedIn →
                </a>
              </div>

              <div v-if="app.notes" class="mb-2">
                <p class="text-xs text-gray-600 italic">"{{ app.notes }}"</p>
              </div>

              <div class="text-xs text-gray-400 mb-2">
                {{ formatDate(app.created_at) }}
              </div>

              <div class="flex flex-wrap gap-1">
                <button
                  v-for="otherStage in stages.filter(s => s.key !== stage.key)"
                  :key="otherStage.key"
                  @click="moveApplication(app.id, otherStage.key)"
                  :disabled="moving === app.id"
                  class="px-2 py-1 text-xs bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  :title="`Déplacer vers ${otherStage.label}`"
                >
                  → {{ otherStage.label }}
                </button>
              </div>
            </div>

            <div v-if="getApplicationsByStage(stage.key).length === 0" class="text-center text-gray-400 text-sm py-8">
              Vide
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const jobId = computed(() => route.params.id as string)

interface Application {
  id: string
  job_id: string
  candidate_id: string
  stage: string
  notes: string | null
  created_at: string
  updated_at: string
  candidate_name: string
  candidate_email: string
  candidate_linkedin_url: string | null
}

const applications = ref<Application[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const moving = ref<string | null>(null)

const stages = [
  { key: 'new', label: 'Nouvelle' },
  { key: 'review', label: 'En revue' },
  { key: 'interview', label: 'Entretien' },
  { key: 'offer', label: 'Offre' },
  { key: 'hired', label: 'Embauché' },
  { key: 'rejected', label: 'Refusé' }
]

const getApplicationsByStage = (stage: string) => {
  return applications.value.filter(app => app.stage === stage)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const moveApplication = async (applicationId: string, newStage: string) => {
  moving.value = applicationId

  try {
    await $fetch(`/api/admin/applications/${applicationId}`, {
      method: 'PATCH',
      body: {
        stage: newStage
      }
    })

    // Refresh applications
    await fetchApplications()
  } catch (err: any) {
    alert(err.data?.message || err.message || 'Erreur lors du déplacement')
  } finally {
    moving.value = null
  }
}

const fetchApplications = async () => {
  try {
    loading.value = true
    error.value = null
    const data = await $fetch<Application[]>(`/api/admin/jobs/${jobId.value}/applications`)
    applications.value = data
  } catch (err: any) {
    error.value = err.data?.message || err.message || 'Erreur lors du chargement des candidatures'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchApplications()
})
</script>

