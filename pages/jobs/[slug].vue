<template>
  <div class="min-h-screen bg-white py-8 sm:py-12">
    <div class="max-w-4xl mx-auto px-6 sm:px-8 lg:px-12">
      <!-- Navigation -->
      <div class="mb-8">
        <NuxtLink
          to="/"
          class="inline-flex items-center text-primary-600 hover:text-primary-900 text-sm font-medium transition-colors group"
        >
          <svg class="w-4 h-4 mr-2 group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
          </svg>
          Back to home
        </NuxtLink>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-900"></div>
        <p class="mt-6 text-primary-600 text-sm">Loading job...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="bg-primary-50 border border-primary-200 rounded-xl p-6 sm:p-8">
        <h2 class="text-primary-900 font-semibold mb-2 text-lg">Error</h2>
        <p class="text-primary-700 mb-4">{{ error }}</p>
        <NuxtLink to="/" class="inline-flex items-center text-primary-600 hover:text-primary-900 text-sm font-medium transition-colors">
          ← Back to home
        </NuxtLink>
      </div>

      <!-- Job details -->
      <div v-else-if="job" class="bg-white rounded-2xl border border-primary-200 overflow-hidden">
        <!-- Header -->
        <div class="bg-primary-900 px-6 sm:px-8 pt-8 sm:pt-10 pb-2 sm:pb-3 text-white">
          <h1 class="text-3xl sm:text-4xl font-semibold mb-2 tracking-tight">{{ job.title }}</h1>
          <div class="flex flex-wrap gap-4 text-primary-300">
            <span v-if="job.location" class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
              {{ job.location }}
            </span>
            <span v-if="job.department" class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-1.5-1.5v18m-9-18v18" />
              </svg>
              {{ job.department }}
            </span>
          </div>
        </div>

        <!-- Job Content -->
        <div class="px-6 sm:px-8 pb-8 sm:pb-10 pt-0">
          <!-- Description from markdown -->
          <div
            v-if="job.description_md"
            class="prose prose-sm sm:prose-base max-w-none
                   prose-headings:text-primary-900
                   prose-headings:font-semibold
                   prose-h2:text-xl
                   prose-h3:text-lg
                   prose-p:text-primary-700
                   prose-p:leading-relaxed
                   prose-a:text-primary-900
                   prose-a:font-medium
                   prose-strong:text-primary-900
                   prose-ul:text-primary-700
                   prose-ul:pl-6
                   prose-li:text-primary-700
                   prose-li:leading-relaxed
                   [&>*]:mt-0
                   [&_*:first-child]:mt-0
                   [&>*+*]:mt-4
                   [&>h2+*]:mt-5
                   [&>h3+*]:mt-4
                   [&>*:first-child]:!mt-0"
            style="margin-top: 0 !important; padding-top: 0 !important;"
            v-html="renderedDescription"
          ></div>

          <!-- Default sections if no markdown -->
          <div v-else class="space-y-10 pt-0">
            <!-- About the company -->
            <section>
              <h2 class="text-2xl font-semibold text-primary-900 mb-5">About the company</h2>
              <p class="text-primary-700 leading-relaxed">We are a fast-growing tech company building innovative solutions.</p>
            </section>

            <!-- The Role -->
            <section>
              <h2 class="text-2xl font-semibold text-primary-900 mb-5">The Role</h2>
              <p class="text-primary-700 leading-relaxed mb-4">Join our team as a {{ job.title }} and help us build the future.</p>
            </section>

            <!-- Responsibilities -->
            <section>
              <h2 class="text-2xl font-semibold text-primary-900 mb-5">Responsibilities</h2>
              <ul class="list-disc list-inside text-primary-700 space-y-2 pl-6">
                <li>Key responsibility 1</li>
                <li>Key responsibility 2</li>
                <li>Key responsibility 3</li>
              </ul>
            </section>

            <!-- Profile / What we're looking for -->
            <section>
              <h2 class="text-2xl font-semibold text-primary-900 mb-5">Profile / What we're looking for</h2>
              <ul class="list-disc list-inside text-primary-700 space-y-2 pl-6">
                <li>Required skill or qualification 1</li>
                <li>Required skill or qualification 2</li>
                <li>Required skill or qualification 3</li>
              </ul>
            </section>

            <!-- What we offer -->
            <section>
              <h2 class="text-2xl font-semibold text-primary-900 mb-5">What we offer</h2>
              <ul class="list-disc list-inside text-primary-700 space-y-2 pl-6">
                <li>Competitive salary and benefits</li>
                <li>Flexible working arrangements</li>
                <li>Growth opportunities</li>
              </ul>
            </section>

            <!-- Practical info -->
            <section>
              <h2 class="text-2xl font-semibold text-primary-900 mb-5">Practical info</h2>
              <div class="space-y-2 text-primary-700">
                <p v-if="job.location"><strong>Location:</strong> {{ job.location }}</p>
                <p v-if="job.department"><strong>Department:</strong> {{ job.department }}</p>
                <p><strong>Type:</strong> Full-time</p>
              </div>
            </section>
          </div>
        </div>

        <!-- Application form -->
        <div class="border-t border-primary-200 px-6 sm:px-8 py-8 sm:py-10 bg-primary-50">
          <h2 class="text-2xl font-semibold mb-8 text-primary-900">Apply for this position</h2>
          
          <form @submit.prevent="submitApplication" class="space-y-5">
            <div>
              <label for="full_name" class="block text-sm font-medium text-primary-900 mb-2">
                Full Name *
              </label>
              <input
                id="full_name"
                v-model="form.full_name"
                type="text"
                required
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="Jean Dupont"
              />
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-primary-900 mb-2">
                Email *
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="jean@example.com"
              />
            </div>

            <div>
              <label for="linkedin_url" class="block text-sm font-medium text-primary-900 mb-2">
                LinkedIn (optional)
              </label>
              <input
                id="linkedin_url"
                v-model="form.linkedin_url"
                type="url"
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="https://www.linkedin.com/in/jean"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-primary-900 mb-2">
                CV
              </label>
              <input
                type="file"
                disabled
                class="w-full px-4 py-3 border border-primary-200 rounded-xl bg-primary-100 text-primary-400 cursor-not-allowed"
              />
            </div>

            <div v-if="submitError" class="bg-primary-100 border border-primary-300 rounded-xl p-4">
              <p class="text-primary-700 text-sm">{{ submitError }}</p>
            </div>

            <button
              type="submit"
              :disabled="submitting"
              class="w-full border-2 border-primary-900 bg-white text-primary-900 py-3.5 px-6 rounded-xl font-medium hover:bg-primary-900 hover:text-white focus:outline-none focus:ring-2 focus:ring-primary-900 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 text-sm"
            >
              <span v-if="submitting">Submitting...</span>
              <span v-else>Submit Application</span>
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
    error.value = err.data?.detail || err.message || 'Error loading job'
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
    submitError.value = err.data?.detail || err.message || 'Error submitting your application'
  } finally {
    submitting.value = false
  }
}
</script>

