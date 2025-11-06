<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Navigation -->
      <div class="mb-6">
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

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Chargement de l'offre...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 class="text-red-800 font-semibold mb-2">Erreur</h2>
        <p class="text-red-600">{{ error }}</p>
        <NuxtLink to="/" class="mt-4 inline-block text-blue-600 hover:underline">
          ← Retour à l'accueil
        </NuxtLink>
      </div>

      <!-- Job details -->
      <div v-else-if="job" class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-8 text-white">
          <h1 class="text-3xl font-bold mb-2">{{ job.title }}</h1>
          <div class="flex flex-wrap gap-4 text-blue-100 mt-4">
            <span v-if="job.location" class="flex items-center gap-1">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {{ job.location }}
            </span>
            <span v-if="job.department" class="flex items-center gap-1">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              {{ job.department }}
            </span>
          </div>
        </div>

        <!-- Description -->
        <div class="px-6 py-6">
          <div 
            v-if="job.description_md" 
            class="prose prose-blue max-w-none"
            v-html="renderedDescription"
          ></div>
          <p v-else class="text-gray-600">Aucune description disponible.</p>
        </div>

        <!-- Application form -->
        <div class="border-t border-gray-200 px-6 py-6 bg-gray-50">
          <h2 class="text-xl font-semibold mb-4">Postuler à cette offre</h2>
          
          <form @submit.prevent="submitApplication" class="space-y-4">
            <div>
              <label for="full_name" class="block text-sm font-medium text-gray-700 mb-1">
                Nom complet *
              </label>
              <input
                id="full_name"
                v-model="form.full_name"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Jean Dupont"
              />
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email *
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="jean@example.com"
              />
            </div>

            <div>
              <label for="linkedin_url" class="block text-sm font-medium text-gray-700 mb-1">
                LinkedIn (optionnel)
              </label>
              <input
                id="linkedin_url"
                v-model="form.linkedin_url"
                type="url"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="https://www.linkedin.com/in/jean"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                CV (bientôt disponible)
              </label>
              <input
                type="file"
                disabled
                class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 text-gray-400 cursor-not-allowed"
              />
              <p class="mt-1 text-xs text-gray-500">L'upload de CV sera disponible prochainement</p>
            </div>

            <div v-if="submitError" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <p class="text-red-600 text-sm">{{ submitError }}</p>
            </div>

            <button
              type="submit"
              :disabled="submitting"
              class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <span v-if="submitting">Envoi en cours...</span>
              <span v-else>Envoyer ma candidature</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { renderMarkdown } from '@/utils/markdown'

const route = useRoute()
const config = useRuntimeConfig()
const router = useRouter()

const slug = computed(() => route.params.slug as string)

interface Job {
  id: string
  slug: string
  title: string
  description_md: string | null
  location: string | null
  department: string | null
  status: string
  created_at: string
}

const job = ref<Job | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const form = ref({
  full_name: '',
  email: '',
  linkedin_url: ''
})

const submitting = ref(false)
const submitError = ref<string | null>(null)

const renderedDescription = computed(() => {
  if (!job.value?.description_md) return ''
  return renderMarkdown(job.value.description_md)
})

// Fetch job details
onMounted(async () => {
  try {
    loading.value = true
    const data = await $fetch<Job>(`${config.public.apiBase}/api/jobs/${slug.value}`)
    job.value = data
  } catch (err: any) {
    error.value = err.data?.detail || err.message || 'Erreur lors du chargement de l\'offre'
  } finally {
    loading.value = false
  }
})

// Submit application
const submitApplication = async () => {
  submitting.value = true
  submitError.value = null

  try {
    await $fetch(`${config.public.apiBase}/api/jobs/${slug.value}/apply`, {
      method: 'POST',
      body: {
        full_name: form.value.full_name,
        email: form.value.email,
        linkedin_url: form.value.linkedin_url || null
      }
    })

    // Redirect to success page
    router.push(`/apply/success?job=${encodeURIComponent(job.value?.title || '')}`)
  } catch (err: any) {
    submitError.value = err.data?.detail || err.message || 'Erreur lors de l\'envoi de votre candidature'
  } finally {
    submitting.value = false
  }
}
</script>

