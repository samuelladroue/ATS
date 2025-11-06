<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">
          Netter ATS
        </h1>
        <p class="text-xl text-gray-600">
          Découvrez nos offres d'emploi et rejoignez notre équipe
        </p>
      </div>

      <!-- Jobs list -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Chargement des offres...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p class="text-red-600">{{ error }}</p>
      </div>

      <div v-else-if="jobs.length === 0" class="text-center py-12">
        <p class="text-gray-600">Aucune offre disponible pour le moment.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="job in jobs"
          :key="job.id"
          class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
        >
          <div class="p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-2">
              {{ job.title }}
            </h2>
            <div class="flex flex-wrap gap-3 text-sm text-gray-600 mb-4">
              <span v-if="job.location" class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ job.location }}
              </span>
              <span v-if="job.department" class="flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                {{ job.department }}
              </span>
            </div>
            <NuxtLink
              :to="`/jobs/${job.slug}`"
              class="inline-block w-full text-center bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
            >
              Voir l'offre et postuler
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Admin link (dev only) -->
      <div class="mt-12 text-center">
        <NuxtLink
          to="/admin/jobs"
          class="text-sm text-gray-500 hover:text-gray-700 inline-flex items-center gap-1"
        >
          Administration
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

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

onMounted(async () => {
  try {
    const data = await $fetch<Job[]>(`${config.public.apiBase}/api/jobs/public`)
    jobs.value = data
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Erreur lors du chargement des offres'
  } finally {
    loading.value = false
  }
})
</script>

