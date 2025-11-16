<template>
  <div class="min-h-screen bg-white py-8 sm:py-12">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <!-- Admin Navigation (includes AI Agent) -->
      <AdminNavigation />
      
      <!-- Header -->
      <div class="mb-10">
        <div class="flex items-start justify-between flex-wrap gap-6">
          <div class="flex-1">
            <h1 class="text-4xl sm:text-5xl font-semibold text-primary-900 mb-3 tracking-tight">All Candidates</h1>
            <p class="text-primary-600 text-lg">View all candidates who have applied to jobs</p>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-900"></div>
        <p class="mt-6 text-primary-600 text-sm">Loading candidates...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-primary-50 border border-primary-200 rounded-xl p-6 sm:p-8">
        <p class="text-primary-700">{{ error }}</p>
      </div>

      <!-- Candidates List -->
      <div v-else-if="candidateRows.length === 0" class="text-center py-20 text-primary-500">
        <p>No applications at the moment.</p>
      </div>

      <div v-else class="bg-white rounded-2xl border border-primary-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-primary-50 border-b border-primary-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">Candidate</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">Email</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">LinkedIn</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">Job</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">Stage</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">Registration Date</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-primary-900 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-primary-200">
              <template v-if="candidateRows.length === 0">
                <tr>
                  <td colspan="7" class="px-6 py-8 text-center text-primary-500">
                    No applications at the moment.
                  </td>
                </tr>
              </template>
              <tr
                v-for="row in candidateRows"
                :key="`${row.candidate.id}-${row.application.id}`"
                class="hover:bg-primary-50 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-semibold text-primary-900">{{ row.candidate.full_name }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <a
                    :href="`mailto:${row.candidate.email}`"
                    class="text-sm text-primary-600 hover:text-primary-900"
                  >
                    {{ row.candidate.email }}
                  </a>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <a
                    v-if="row.candidate.linkedin_url"
                    :href="row.candidate.linkedin_url"
                    target="_blank"
                    rel="noopener"
                    class="inline-flex items-center text-primary-600 hover:text-primary-900"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                  </a>
                  <span v-else class="text-sm text-primary-400">-</span>
                </td>
                <td class="px-6 py-4">
                  <NuxtLink
                    v-if="row.job"
                    :to="`/admin/jobs/${row.application.job_id}`"
                    class="text-sm font-medium text-primary-600 hover:text-primary-900 hover:underline"
                  >
                    {{ row.job.title }}
                  </NuxtLink>
                  <span v-else class="text-sm text-primary-400">Job deleted</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-700 border border-primary-200"
                  >
                    {{ getStageLabel(row.application.stage) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-primary-600">{{ formatDate(row.candidate.created_at) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <button
                    @click="confirmDeleteCandidate(row.candidate)"
                    class="inline-flex items-center border-2 border-red-600 text-red-600 py-2 px-4 rounded-xl font-medium hover:bg-red-600 hover:text-white transition-all duration-200 text-sm"
                    title="Delete candidate"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Application {
  id: string
  job_id: string
  candidate_id: string
  stage: string
  notes: string | null
  created_at: string
  updated_at: string
}

interface Candidate {
  id: string
  email: string
  full_name: string
  linkedin_url: string | null
  created_at: string
  updated_at: string | null
  applications: Application[]
}

interface Job {
  id: string
  title: string
}

interface CandidateRow {
  candidate: Candidate
  application: Application
  job: Job | null
}

const candidates = ref<Candidate[]>([])
const jobs = ref<Job[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const deleting = ref(false)

// Compute candidate rows (one row per application)
const candidateRows = computed<CandidateRow[]>(() => {
  const rows: CandidateRow[] = []
  for (const candidate of candidates.value) {
    for (const application of candidate.applications) {
      const job = jobs.value.find(j => j.id === application.job_id) || null
      rows.push({
        candidate,
        application,
        job
      })
    }
  }
  return rows
})

// Fetch candidates and jobs
const fetchCandidates = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Fetch both candidates and jobs in parallel
    const [candidatesData, jobsData] = await Promise.all([
      $fetch<Candidate[]>('/api/admin/candidates'),
      $fetch<Job[]>('/api/admin/jobs')
    ])
    
    candidates.value = candidatesData
    jobs.value = jobsData
  } catch (err: any) {
    error.value = err.data?.message || err.message || 'Error loading candidates'
  } finally {
    loading.value = false
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

// Get stage label
const getStageLabel = (stage: string) => {
  const stageLabels: Record<string, string> = {
    'new': 'New applicants',
    'review': 'Screening interview',
    'interview': 'Technical interview',
    'offer': 'Offer sent',
    'hired': 'Hired',
    'rejected': 'Refused'
  }
  return stageLabels[stage] || stage
}

// Delete candidate
const confirmDeleteCandidate = (candidate: Candidate) => {
  const applicationsCount = candidate.applications.length
  const applicationsText = applicationsCount > 0 
    ? ` This will also delete ${applicationsCount} associated application${applicationsCount > 1 ? 's' : ''} and cannot be undone.`
    : ' This action cannot be undone.'
  
  if (confirm(`Are you sure you want to delete candidate "${candidate.full_name}" (${candidate.email})?${applicationsText}`)) {
    deleteCandidate(candidate.id)
  }
}

const deleteCandidate = async (candidateId: string) => {
  deleting.value = true
  try {
    await $fetch(`/api/admin/candidates/${candidateId}`, {
      method: 'DELETE'
    })
    await fetchCandidates()
  } catch (err: any) {
    alert(err.data?.message || err.message || 'Error deleting candidate')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  fetchCandidates()
})
</script>

