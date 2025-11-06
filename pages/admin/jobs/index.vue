<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="mb-4">
          <NuxtLink
            to="/"
            class="inline-flex items-center text-blue-600 hover:text-blue-700 text-sm font-medium"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Retour à l'accueil
          </NuxtLink>
        </div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Gestion des offres d'emploi</h1>
        <p class="text-gray-600">Créez et gérez vos offres d'emploi</p>
      </div>

      <!-- Create job form -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
        <h2 class="text-xl font-semibold mb-4">Créer une nouvelle offre</h2>
        
        <form @submit.prevent="createJob" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="slug" class="block text-sm font-medium text-gray-700 mb-1">
                Slug * (ex: software-engineer)
              </label>
              <input
                id="slug"
                v-model="newJob.slug"
                type="text"
                required
                pattern="[a-z0-9-]+"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="software-engineer"
              />
            </div>

            <div>
              <label for="title" class="block text-sm font-medium text-gray-700 mb-1">
                Titre *
              </label>
              <input
                id="title"
                v-model="newJob.title"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Software Engineer"
              />
            </div>
          </div>

          <div>
            <label for="description_md" class="block text-sm font-medium text-gray-700 mb-1">
              Description (Markdown)
            </label>
            <textarea
              id="description_md"
              v-model="newJob.description_md"
              rows="6"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="## Missions&#10;- Développer des APIs&#10;- Travailler avec FastAPI"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label for="location" class="block text-sm font-medium text-gray-700 mb-1">
                Localisation
              </label>
              <input
                id="location"
                v-model="newJob.location"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Paris"
              />
            </div>

            <div>
              <label for="department" class="block text-sm font-medium text-gray-700 mb-1">
                Département
              </label>
              <input
                id="department"
                v-model="newJob.department"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Engineering"
              />
            </div>

            <div>
              <label for="status" class="block text-sm font-medium text-gray-700 mb-1">
                Statut
              </label>
              <select
                id="status"
                v-model="newJob.status"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="open">Ouverte</option>
                <option value="closed">Fermée</option>
              </select>
            </div>
          </div>

          <div v-if="createError" class="bg-red-50 border border-red-200 rounded-lg p-3">
            <p class="text-red-600 text-sm">{{ createError }}</p>
          </div>

          <button
            type="submit"
            :disabled="creating"
            class="bg-blue-600 text-white py-2 px-6 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="creating">Création...</span>
            <span v-else>Créer l'offre</span>
          </button>
        </form>
      </div>

      <!-- Jobs list -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xl font-semibold">Liste des offres</h2>
        </div>

        <div v-if="loading" class="p-12 text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-600">Chargement...</p>
        </div>

        <div v-else-if="error" class="p-6 bg-red-50 border border-red-200 m-6 rounded-lg">
          <p class="text-red-600">{{ error }}</p>
        </div>

        <div v-else-if="jobs.length === 0" class="p-12 text-center text-gray-500">
          <p>Aucune offre pour le moment.</p>
        </div>

        <div v-else class="divide-y divide-gray-200">
          <div
            v-for="job in jobs"
            :key="job.id"
            class="px-6 py-4 hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-semibold text-gray-900">
                    {{ job.title }}
                  </h3>
                  <span
                    :class="[
                      'px-2 py-1 text-xs font-medium rounded-full',
                      job.status === 'open' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    ]"
                  >
                    {{ job.status === 'open' ? 'Ouverte' : 'Fermée' }}
                  </span>
                </div>
                <div class="mt-1 flex items-center gap-4 text-sm text-gray-600">
                  <span v-if="job.location">{{ job.location }}</span>
                  <span v-if="job.department">{{ job.department }}</span>
                  <span class="text-gray-400">
                    {{ formatDate(job.created_at) }}
                  </span>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <NuxtLink
                  :to="`/admin/jobs/${job.id}`"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  Voir candidatures
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Job {
  id: string
  slug: string
  title: string
  location: string | null
  department: string | null
  status: string
  created_at: string
}

const jobs = ref<Job[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const newJob = ref({
  slug: '',
  title: '',
  description_md: '',
  location: '',
  department: '',
  status: 'open'
})

const creating = ref(false)
const createError = ref<string | null>(null)

// Fetch jobs
const fetchJobs = async () => {
  try {
    loading.value = true
    error.value = null
    const data = await $fetch<Job[]>('/api/admin/jobs')
    jobs.value = data
  } catch (err: any) {
    error.value = err.data?.message || err.message || 'Erreur lors du chargement des offres'
  } finally {
    loading.value = false
  }
}

// Create job
const createJob = async () => {
  creating.value = true
  createError.value = null

  try {
    const jobData = {
      slug: newJob.value.slug,
      title: newJob.value.title,
      description_md: newJob.value.description_md || null,
      location: newJob.value.location || null,
      department: newJob.value.department || null,
      status: newJob.value.status
    }

    await $fetch('/api/admin/jobs', {
      method: 'POST',
      body: jobData
    })

    // Reset form
    newJob.value = {
      slug: '',
      title: '',
      description_md: '',
      location: '',
      department: '',
      status: 'open'
    }

    // Refresh list
    await fetchJobs()
  } catch (err: any) {
    createError.value = err.data?.message || err.message || 'Erreur lors de la création de l\'offre'
  } finally {
    creating.value = false
  }
}

// Format date
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchJobs()
})
</script>

