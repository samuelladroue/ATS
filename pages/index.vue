<template>
  <div class="min-h-screen bg-white">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 py-16 sm:py-20">
      <!-- Header -->
      <div class="text-center mb-16 sm:mb-20">
        <h1 class="text-5xl sm:text-6xl font-semibold text-primary-900 mb-6 tracking-tight">
          Netter ATS
        </h1>
        <p class="text-lg sm:text-xl text-primary-600 font-light max-w-2xl mx-auto">
          Découvrez nos offres d'emploi et rejoignez notre équipe
        </p>
      </div>

      <!-- Jobs list -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-900"></div>
        <p class="mt-6 text-primary-600 text-sm">Chargement des offres...</p>
      </div>

      <div v-else-if="error" class="bg-primary-50 border border-primary-200 rounded-xl p-6 text-center max-w-md mx-auto">
        <p class="text-primary-700 text-sm">{{ error }}</p>
      </div>

      <div v-else-if="jobs.length === 0" class="text-center py-20">
        <p class="text-primary-600">Aucune offre disponible pour le moment.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <NuxtLink
          v-for="job in jobs"
          :key="job.id"
          :to="`/jobs/${job.slug}`"
          class="bg-white rounded-2xl border-2 border-primary-200 overflow-hidden hover:border-primary-900 hover:shadow-soft transition-all duration-200 group block"
        >
          <div class="p-6 sm:p-8">
            <h2 class="text-xl sm:text-2xl font-semibold text-primary-900 mb-4 group-hover:text-primary-800 transition-colors">
              {{ job.title }}
            </h2>
            <div class="flex flex-wrap gap-3 text-sm text-primary-600 mb-6">
              <span v-if="job.location" class="flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
                {{ job.location }}
              </span>
              <span v-if="job.department" class="flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-1.5-1.5v18m-9-18v18" />
                </svg>
                {{ job.department }}
              </span>
            </div>
            <div class="mt-6 pt-6 border-t border-primary-200">
              <div class="inline-flex items-center justify-center w-full border-2 border-primary-900 text-primary-900 py-3 px-6 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-sm">
                Learn more
                <svg class="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
              </div>
            </div>
          </div>
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
    const data = await $fetch<Job[]>('/api/jobs/public')
    jobs.value = data
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Erreur lors du chargement des offres'
  } finally {
    loading.value = false
  }
})
</script>

