<template>
  <div class="min-h-screen bg-white py-8 sm:py-12">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <!-- Admin Navigation (includes AI Agent) -->
      <AdminNavigation />
      
      <!-- Header -->
      <div class="mb-10">
        <div class="flex items-start justify-between flex-wrap gap-6 mb-6">
          <div class="flex-1">
            <h1 class="text-4xl sm:text-5xl font-semibold text-primary-900 mb-3 tracking-tight">Job Management</h1>
            <p class="text-primary-600 text-lg">Create and manage your job offers</p>
          </div>
          <button
            @click="showCreateForm = !showCreateForm"
            class="w-full mb-3 inline-flex items-center justify-center border-2 border-primary-900 text-primary-900 py-2 px-4 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-sm whitespace-nowrap shrink-0"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" :d="showCreateForm ? 'M6 18L18 6M6 6l12 12' : 'M12 4v16m8-8H4'" />
            </svg>
            {{ showCreateForm ? 'Hide form' : 'Create new job' }}
          </button>
        </div>
      </div>

      <!-- Create job form -->
      <div v-if="showCreateForm" class="bg-white rounded-2xl border border-primary-200 p-6 sm:p-8 mb-10">
        <h2 class="text-2xl font-semibold mb-6 text-primary-900">Create new job</h2>
        
        <form @submit.prevent="createJob" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label for="slug" class="block text-sm font-medium text-primary-900 mb-2">
                Slug * (ex: software-engineer)
              </label>
              <input
                id="slug"
                v-model="newJob.slug"
                type="text"
                required
                pattern="[a-z0-9-]+"
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="software-engineer"
              />
            </div>

            <div>
              <label for="title" class="block text-sm font-medium text-primary-900 mb-2">
                Title *
              </label>
              <input
                id="title"
                v-model="newJob.title"
                type="text"
                required
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="Software Engineer"
              />
            </div>
          </div>

          <div>
            <label for="description_md" class="block text-sm font-medium text-primary-900 mb-2">
              Description (Markdown)
            </label>
            <textarea
              id="description_md"
              v-model="newJob.description_md"
              rows="6"
              class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all resize-none"
              placeholder="## Missions&#10;- Développer des APIs&#10;- Travailler avec FastAPI"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label for="location" class="block text-sm font-medium text-primary-900 mb-2">
                Location
              </label>
              <input
                id="location"
                v-model="newJob.location"
                type="text"
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="Paris"
              />
            </div>

            <div>
              <label for="department" class="block text-sm font-medium text-primary-900 mb-2">
                Department
              </label>
              <input
                id="department"
                v-model="newJob.department"
                type="text"
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 transition-all"
                placeholder="Engineering"
              />
            </div>

            <div>
              <label for="status" class="block text-sm font-medium text-primary-900 mb-2">
                Status
              </label>
              <select
                id="status"
                v-model="newJob.status"
                class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 transition-all"
              >
                <option value="open">Open</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>

          <div v-if="createError" class="bg-primary-100 border border-primary-300 rounded-xl p-4">
            <p class="text-primary-700 text-sm">{{ createError }}</p>
          </div>

          <button
            type="submit"
            :disabled="creating"
            :class="[
              'px-4 py-3 border-2 border-primary-900 rounded-xl font-medium transition-all duration-200 text-sm',
              creating
                ? 'bg-primary-200 text-primary-500 cursor-not-allowed border-primary-300'
                : 'bg-white text-primary-900 hover:bg-primary-900 hover:text-white'
            ]"
          >
            <span v-if="creating">Creating...</span>
            <span v-else>Create job</span>
          </button>
        </form>
      </div>

      <!-- Jobs list -->
      <div class="bg-white rounded-2xl border border-primary-200 overflow-hidden">
        <div class="px-6 sm:px-8 py-5 border-b border-primary-200">
          <h2 class="text-xl font-semibold text-primary-900">Job List</h2>
        </div>

        <div v-if="loading" class="p-16 text-center">
          <div class="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-900"></div>
          <p class="mt-6 text-primary-600 text-sm">Loading...</p>
        </div>

        <div v-else-if="error" class="p-6 bg-primary-100 border border-primary-300 m-6 rounded-xl">
          <p class="text-primary-700">{{ error }}</p>
        </div>

        <div v-else-if="jobs.length === 0" class="p-16 text-center text-primary-500">
          <p>No jobs at the moment.</p>
        </div>

        <div v-else class="divide-y divide-primary-200">
          <div
            v-for="job in jobs"
            :key="job.id"
            class="px-6 sm:px-8 py-5 hover:bg-primary-50 transition-colors"
          >
            <div class="flex items-center justify-between flex-wrap gap-4">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-3 flex-wrap mb-2">
                  <h3 class="text-lg font-semibold text-primary-900">
                    {{ job.title }}
                  </h3>
                  <span
                    :class="[
                      'px-2.5 py-1 text-xs font-medium rounded-full',
                      job.status === 'open' 
                        ? 'bg-primary-100 text-primary-700 border border-primary-200' 
                        : 'bg-primary-200 text-primary-600 border border-primary-300'
                    ]"
                  >
                    {{ job.status === 'open' ? 'Open' : 'Closed' }}
                  </span>
                </div>
                <div class="flex items-center gap-4 text-sm text-primary-600 flex-wrap">
                  <span v-if="job.location">{{ job.location }}</span>
                  <span v-if="job.department">{{ job.department }}</span>
                  <span class="text-primary-400">
                    {{ formatDate(job.created_at) }}
                  </span>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <NuxtLink
                  :to="`/admin/jobs/${job.id}`"
                  class="inline-flex items-center border-2 border-primary-900 text-primary-900 py-3 px-6 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-sm group"
                >
                  Learn more
                  <svg class="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                  </svg>
                </NuxtLink>
                <button
                  @click="confirmDeleteJob(job)"
                  class="inline-flex items-center border-2 border-red-600 text-red-600 py-3 px-6 rounded-xl font-medium hover:bg-red-600 hover:text-white transition-all duration-200 text-sm"
                  title="Delete job"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
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
const showCreateForm = ref(false)

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
const jobToDelete = ref<Job | null>(null)
const deleting = ref(false)

// Fetch jobs
const fetchJobs = async () => {
  try {
    loading.value = true
    error.value = null
    const data = await $fetch<Job[]>('/api/admin/jobs')
    jobs.value = data
  } catch (err: any) {
    error.value = err.data?.message || err.message || 'Error loading jobs'
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

    // Close form
    showCreateForm.value = false

    // Refresh list
    await fetchJobs()
  } catch (err: any) {
    createError.value = err.data?.message || err.message || 'Error creating job'
  } finally {
    creating.value = false
  }
}

// Format date
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// Delete job
const confirmDeleteJob = (job: Job) => {
  if (confirm(`Are you sure you want to delete the job "${job.title}"? This will also delete all associated applications and cannot be undone.`)) {
    deleteJob(job.id)
  }
}

const deleteJob = async (jobId: string) => {
  deleting.value = true
  try {
    await $fetch(`/api/admin/jobs/${jobId}`, {
      method: 'DELETE'
    })
    await fetchJobs()
  } catch (err: any) {
    alert(err.data?.message || err.message || 'Error deleting job')
  } finally {
    deleting.value = false
    jobToDelete.value = null
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

