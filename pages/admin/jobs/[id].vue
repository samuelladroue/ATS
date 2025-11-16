<template>
  <div class="min-h-screen bg-white py-8 sm:py-12">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <!-- Admin Navigation (includes AI Agent) -->
      <AdminNavigation />
      
      <!-- Header -->
      <div class="mb-10">
        <div class="mb-6">
          <NuxtLink
            to="/admin/jobs"
            class="inline-flex items-center text-primary-600 hover:text-primary-900 text-sm font-medium transition-colors group"
          >
            <svg class="w-4 h-4 mr-2 group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            Back to jobs
          </NuxtLink>
        </div>
        <h1 class="text-4xl sm:text-5xl font-semibold text-primary-900 mb-2 tracking-tight">
          {{ job?.title || 'Applications' }}
        </h1>
        <div v-if="job" class="flex items-center gap-2 text-primary-600 flex-wrap">
          <span v-if="job.location">{{ job.location }}</span>
          <span v-if="job.location && job.department" class="text-primary-300">•</span>
          <span v-if="job.department">{{ job.department }}</span>
        </div>
        <p v-else class="text-primary-600">Job ID: {{ jobId }}</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-900"></div>
        <p class="mt-6 text-primary-600 text-sm">Loading applications...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-primary-50 border border-primary-200 rounded-xl p-6 sm:p-8">
        <p class="text-primary-700">{{ error }}</p>
      </div>

      <!-- Kanban board -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 sm:gap-6">
        <div
          v-for="(stage, index) in stages"
          :key="stage.key"
          class="bg-white rounded-2xl border border-primary-200"
        >
          <div class="px-4 sm:px-5 py-4 border-b border-primary-200">
            <h3 class="font-semibold text-primary-900 text-sm">{{ stage.label }}</h3>
            <p class="text-xs text-primary-500 mt-1">
              {{ getApplicationsByStage(stage.key).length }} application(s)
            </p>
          </div>

          <div class="p-3 sm:p-4 space-y-3 min-h-[200px]">
            <div
              v-for="app in getApplicationsByStage(stage.key)"
              :key="app.id"
              class="bg-primary-50 rounded-xl p-3 sm:p-4 border border-primary-200 hover:border-primary-300 transition-all"
            >
              <div class="mb-3">
                <div class="flex items-center gap-2 mb-1">
                  <p class="font-semibold text-sm text-primary-900">{{ app.candidate_name }}</p>
                  <span class="w-6 h-6 flex items-center justify-center bg-primary-900 text-white text-xs font-semibold rounded-lg">
                    {{ getStageNumber(app.stage) }}
                  </span>
                </div>
                <div v-if="app.candidate_linkedin_url" class="mb-2">
                  <a
                    :href="app.candidate_linkedin_url"
                    target="_blank"
                    rel="noopener"
                    class="inline-flex items-center justify-center w-6 h-6 text-primary-600 hover:text-primary-900 transition-colors"
                    title="LinkedIn"
                  >
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                  </a>
                </div>
                
                <!-- Notes summary -->
                <div v-if="getAllNotesForApplication(app).length > 0" class="mt-2 pt-2 border-t border-primary-200">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs text-primary-500 font-medium">Notes:</span>
                    <div class="flex items-center gap-1 flex-wrap">
                      <span
                        v-for="(note, idx) in getAllNotesForApplication(app).slice(0, 4)"
                        :key="idx"
                        :class="[
                          'px-1.5 py-0.5 rounded text-xs font-semibold',
                          note.rating >= 3
                            ? 'bg-green-100 text-green-700 border border-green-300'
                            : 'bg-red-100 text-red-700 border border-red-300'
                        ]"
                        :title="`${note.rating}/4${note.report ? ' - ' + note.report.substring(0, 50) + '...' : ''}`"
                      >
                        {{ note.rating }}/4
                      </span>
                      <span v-if="getAllNotesForApplication(app).length > 4" class="text-xs text-primary-400">
                        +{{ getAllNotesForApplication(app).length - 4 }}
                      </span>
                    </div>
                    <span
                      v-if="getAverageRating(app) > 0"
                      :class="[
                        'text-xs font-semibold px-1.5 py-0.5 rounded',
                        getAverageRating(app) >= 3
                          ? 'bg-green-50 text-green-700 border border-green-200'
                          : 'bg-red-50 text-red-700 border border-red-200'
                      ]"
                    >
                      Avg: {{ getAverageRating(app).toFixed(1) }}
                    </span>
                  </div>
                </div>
              </div>

              <button
                @click="openModal(app)"
                class="w-full mb-3 inline-flex items-center justify-center border-2 border-primary-900 text-primary-900 py-2 px-4 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-xs"
              >
                View details
              </button>

              <div class="flex gap-1 justify-center flex-wrap">
                <button
                  v-for="(stageOption, idx) in stages"
                  :key="`${app.id}-${stageOption.key}-${idx}`"
                  @click="moveApplication(app.id, stageOption.key)"
                  :disabled="moving === app.id"
                  :class="[
                    'w-8 h-8 flex items-center justify-center text-xs font-semibold rounded-lg transition-all duration-200 shrink-0 border-2',
                    isCurrentStage(app.stage, stageOption.key)
                      ? 'bg-white text-primary-900 border-primary-900 shadow-md border-4 scale-110'
                      : 'bg-white border-primary-300 text-primary-700 hover:bg-primary-900 hover:text-white hover:border-primary-900',
                    moving === app.id ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                  ]"
                  :title="isCurrentStage(app.stage, stageOption.key) ? `Current stage: ${stageOption.label}` : `Move to ${stageOption.label}`"
                >
                  {{ idx + 1 }}
                </button>
              </div>
            </div>

            <div v-if="getApplicationsByStage(stage.key).length === 0" class="text-center text-primary-400 text-sm py-8">
              Empty
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="selectedApplication"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click.self="closeModal"
    >
      <div class="bg-white rounded-2xl w-full max-w-6xl max-h-[90vh] flex flex-col border border-primary-200">
        <!-- Header -->
        <div class="flex-shrink-0 border-b border-primary-200 px-6 py-4 flex items-center justify-between">
          <h2 class="text-2xl font-semibold text-primary-900">Application Details</h2>
          <button
            @click="closeModal"
            class="text-primary-600 hover:text-primary-900 transition-colors"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Two column layout -->
        <div class="flex flex-1 overflow-hidden">
          <!-- Left column: Candidate details (fixed) -->
          <div class="w-80 flex-shrink-0 border-r border-primary-200 px-6 py-6 overflow-y-auto">
            <div class="space-y-6">
              <div>
                <h3 class="text-sm font-medium text-primary-500 mb-1">Full Name</h3>
                <p class="text-lg font-semibold text-primary-900">{{ selectedApplication.candidate_name }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-primary-500 mb-1">Email</h3>
                <p class="text-primary-900 break-words">{{ selectedApplication.candidate_email }}</p>
              </div>
              <div v-if="selectedApplication.candidate_linkedin_url">
                <h3 class="text-sm font-medium text-primary-500 mb-1">LinkedIn</h3>
                <a
                  :href="selectedApplication.candidate_linkedin_url"
                  target="_blank"
                  rel="noopener"
                  class="text-primary-600 hover:text-primary-900 font-medium inline-flex items-center gap-2 break-words"
                >
                  <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                  </svg>
                  <span class="break-all">{{ selectedApplication.candidate_linkedin_url }}</span>
                </a>
              </div>
              <div>
                <h3 class="text-sm font-medium text-primary-500 mb-1">Application Date</h3>
                <p class="text-primary-900">{{ formatDate(selectedApplication.created_at) }}</p>
              </div>
              <div class="mb-6">
                <button
                  @click="showEmailComposer = true"
                  class="w-full mb-3 inline-flex items-center justify-center border-2 border-primary-900 text-primary-900 py-2 px-4 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-sm"
                >
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  Send email
                </button>
              </div>
              <div>
                <h3 class="text-sm font-medium text-primary-500 mb-3">Change stage</h3>
                <div class="flex flex-col gap-2">
                  <button
                    v-for="stage in stages"
                    :key="stage.key"
                    @click="moveApplication(selectedApplication!.id, stage.key)"
                    :disabled="moving === selectedApplication!.id"
                    :class="[
                      'rounded-xl font-medium text-sm transition-all duration-200 text-left border-2',
                      selectedApplication && isCurrentStage(selectedApplication.stage, stage.key)
                        ? 'bg-white text-primary-900 border-primary-900 px-5 py-3 font-semibold shadow-lg scale-105 border-4'
                        : 'bg-white border-primary-300 text-primary-900 hover:bg-primary-50 hover:border-primary-400 px-4 py-2',
                      moving === selectedApplication!.id ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                    ]"
                  >
                    {{ stage.label }}
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Right column: Notes and reports (scrollable) -->
          <div class="flex-1 px-6 py-6 overflow-y-auto">
            <div class="max-w-3xl">
              <!-- Email History Section -->
              <div class="mb-8">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-semibold text-primary-900">Email History</h3>
                  <button
                    @click="refreshEmailHistory"
                    class="text-sm text-primary-600 hover:text-primary-900 transition-colors"
                  >
                    Refresh
                  </button>
                </div>
                <div v-if="loadingEmails" class="text-center py-4">
                  <div class="inline-block animate-spin rounded-full h-6 w-6 border-2 border-primary-200 border-t-primary-900"></div>
                </div>
                <div v-else-if="emailHistory.length === 0" class="text-center py-8 text-primary-500 text-sm">
                  No emails sent to this candidate
                </div>
                <div v-else class="space-y-4">
                  <div
                    v-for="email in emailHistory"
                    :key="email.id"
                    class="bg-primary-50 rounded-xl p-4 border border-primary-200"
                  >
                    <div class="flex items-start justify-between mb-2">
                      <div>
                        <p class="font-semibold text-primary-900 text-sm">{{ email.subject }}</p>
                        <p class="text-xs text-primary-600 mt-1">
                          From: {{ email.sender_name || email.sender_email }}
                        </p>
                      </div>
                      <span class="text-xs text-primary-500 whitespace-nowrap ml-4">
                        {{ formatDate(email.created_at) }}
                      </span>
                    </div>
                    <div class="text-sm text-primary-700 whitespace-pre-wrap mt-2">{{ email.body }}</div>
                  </div>
                </div>
              </div>

              <h3 class="text-lg font-semibold text-primary-900 mb-6">Notes and Reports</h3>
              
              <!-- Notes for each stage -->
              <div class="space-y-6">
                <div
                  v-for="stage in stages"
                  :key="stage.key"
                  class="border border-primary-200 rounded-xl p-5"
                >
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="font-semibold text-primary-900 text-base">{{ stage.label }}</h4>
                    <span class="text-xs text-primary-500 bg-primary-50 px-2 py-1 rounded-lg">
                      {{ getStageNotes(stage.key).length }} note(s)
                    </span>
                  </div>
                  
                  <!-- Existing notes for this stage -->
                  <div v-if="getStageNotes(stage.key).length > 0" class="space-y-3 mb-4">
                    <div
                      v-for="(note, noteIdx) in getStageNotes(stage.key)"
                      :key="noteIdx"
                      class="bg-primary-50 rounded-lg p-4 border border-primary-200"
                    >
                      <div class="flex items-center justify-between mb-2">
                        <div class="flex items-center gap-2 flex-wrap">
                          <span
                            :class="[
                              'px-2.5 py-1 rounded-lg text-xs font-semibold',
                              note.rating >= 3
                                ? 'bg-green-100 text-green-700 border border-green-300'
                                : 'bg-red-100 text-red-700 border border-red-300'
                            ]"
                          >
                            Note: {{ note.rating }}/4
                          </span>
                          <span v-if="note.interviewer" class="text-xs text-primary-500">
                            par {{ note.interviewer }}
                          </span>
                        </div>
                        <span class="text-xs text-primary-400">
                          {{ formatDate(note.created_at) }}
                        </span>
                      </div>
                      <p class="text-sm text-primary-700 whitespace-pre-wrap mt-2">{{ note.report }}</p>
                    </div>
                  </div>
                  
                  <!-- Add note form for this stage -->
                  <div class="border-t border-primary-200 pt-4">
                    <div class="space-y-4">
                      <div>
                        <label class="block text-sm font-medium text-primary-700 mb-2">
                          Report
                        </label>
                        <textarea
                          v-model="stageNoteForms[stage.key].report"
                          rows="4"
                          class="w-full px-4 py-3 border border-primary-300 rounded-lg focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 text-sm resize-none"
                          placeholder="Add a report for this stage..."
                        ></textarea>
                      </div>
                      <div class="grid grid-cols-2 gap-4">
                        <div>
                          <label class="block text-sm font-medium text-primary-700 mb-2">
                            Note sur 4
                          </label>
                          <div class="flex gap-2">
                            <button
                              v-for="rating in [1, 2, 3, 4]"
                              :key="rating"
                              @click="stageNoteForms[stage.key].rating = rating"
                              :class="[
                                'w-12 h-12 rounded-lg font-semibold text-sm transition-all duration-200 border-2',
                                stageNoteForms[stage.key].rating === rating
                                  ? rating >= 3
                                    ? 'bg-green-500 text-white border-green-600 shadow-md'
                                    : 'bg-red-500 text-white border-red-600 shadow-md'
                                  : rating >= 3
                                    ? 'bg-white border-green-300 text-green-700 hover:bg-green-50'
                                    : 'bg-white border-red-300 text-red-700 hover:bg-red-50'
                              ]"
                            >
                              {{ rating }}
                            </button>
                          </div>
                        </div>
                        <div>
                          <label class="block text-sm font-medium text-primary-700 mb-2">
                            Interviewer (optionnel)
                          </label>
                          <input
                            v-model="stageNoteForms[stage.key].interviewer"
                            type="text"
                            class="w-full px-4 py-3 border border-primary-300 rounded-lg focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 text-sm"
                            placeholder="Nom de l'interviewer"
                          />
                        </div>
                      </div>
                      
                      <!-- Validation indicator -->
                      <div v-if="!stageNoteForms[stage.key].report || !stageNoteForms[stage.key].rating" class="text-xs text-primary-500 bg-primary-50 border border-primary-200 rounded-lg p-2">
                        <div class="flex items-center gap-2">
                          <svg class="w-4 h-4 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span v-if="!stageNoteForms[stage.key].report && !stageNoteForms[stage.key].rating">
                            Please fill in the report and select a rating
                          </span>
                          <span v-else-if="!stageNoteForms[stage.key].report">
                            Please fill in the report
                          </span>
                          <span v-else-if="!stageNoteForms[stage.key].rating">
                            Please select a rating
                          </span>
                        </div>
                      </div>
                      
                      <!-- Submit button -->
                      <button
                        @click="addStageNote(stage.key)"
                        :disabled="!stageNoteForms[stage.key].report || !stageNoteForms[stage.key].rating || savingNotes"
                        :class="[
                          'w-full py-2 px-4 border-2 border-primary-900 rounded-xl font-medium text-sm transition-all duration-200 flex items-center justify-center gap-2',
                          (!stageNoteForms[stage.key].report || !stageNoteForms[stage.key].rating || savingNotes)
                            ? 'bg-primary-200 text-primary-500 cursor-not-allowed border-primary-300'
                            : 'bg-white text-primary-900 hover:bg-primary-900 hover:text-white'
                        ]"
                      >
                        <svg v-if="!savingNotes" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                        </svg>
                        <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span>{{ savingNotes ? 'Saving...' : 'Save note' }}</span>
                      </button>
                      
                      <!-- Success message (temporary) -->
                      <div v-if="noteSavedSuccessfully === stage.key" class="text-xs text-green-700 bg-green-50 border border-green-200 rounded-lg p-2 flex items-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Note saved successfully!</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Email Composer Modal -->
  <div
    v-if="showEmailComposer"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    @click.self="showEmailComposer = false"
  >
    <div class="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] flex flex-col border border-primary-200">
      <!-- Header -->
      <div class="flex-shrink-0 border-b border-primary-200 px-6 py-4 flex items-center justify-between">
        <h2 class="text-2xl font-semibold text-primary-900">Send email</h2>
        <button
          @click="showEmailComposer = false"
          class="text-primary-600 hover:text-primary-900 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Content -->
      <div class="flex-1 px-6 py-6 overflow-y-auto">
        <form @submit.prevent="sendEmail" class="space-y-5">
          <!-- Template Selection -->
          <div>
            <label class="block text-sm font-medium text-primary-900 mb-2">
              Template (optional)
            </label>
            <div class="flex gap-2">
              <select
                v-model="emailForm.selectedTemplateId"
                @change="loadTemplate"
                class="flex-1 px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900"
              >
                <option value="">No template</option>
                <option v-for="template in emailTemplates" :key="template.id" :value="template.id">
                  {{ template.name }}
                </option>
              </select>
              <NuxtLink
                to="/admin/email-templates"
                class="px-4 py-3 border-2 border-primary-900 text-primary-900 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 whitespace-nowrap bg-white inline-flex items-center justify-center"
              >
                Manage templates
              </NuxtLink>
            </div>
          </div>

          <!-- Subject -->
          <div>
            <label class="block text-sm font-medium text-primary-900 mb-2">
              Subject *
            </label>
            <input
              v-model="emailForm.subject"
              type="text"
              required
              class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400"
              placeholder="Email subject"
            />
          </div>

          <!-- Body -->
          <div>
            <label class="block text-sm font-medium text-primary-900 mb-2">
              Message *
            </label>
            <textarea
              v-model="emailForm.body"
              rows="10"
              required
              class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 resize-none"
              placeholder="Email body (you can use {{candidate_name}} for the candidate's name)"
            ></textarea>
            <p class="text-xs text-primary-500 mt-2">
              Tip: Use <code class="bg-primary-100 px-1 rounded">{{candidate_name}}</code> to insert the candidate's name
            </p>
          </div>

          <!-- Preview -->
          <div v-if="emailForm.subject || emailForm.body" class="bg-primary-50 rounded-xl p-4 border border-primary-200">
            <p class="text-xs font-medium text-primary-700 mb-2">Preview:</p>
            <p class="text-sm font-semibold text-primary-900 mb-2">{{ emailForm.subject || '(No subject)' }}</p>
            <div class="text-sm text-primary-700 whitespace-pre-wrap">{{ previewEmailBody }}</div>
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="showEmailComposer = false"
              class="flex-1 px-4 py-3 border-2 border-primary-900 text-primary-900 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 bg-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="sendingEmail || !emailForm.subject || !emailForm.body"
              :class="[
                'flex-1 px-4 py-3 border-2 border-primary-900 rounded-xl font-medium transition-all duration-200',
                sendingEmail || !emailForm.subject || !emailForm.body
                  ? 'bg-primary-200 text-primary-500 cursor-not-allowed border-primary-300'
                  : 'bg-white text-primary-900 hover:bg-primary-900 hover:text-white'
              ]"
            >
              <span v-if="sendingEmail">Sending...</span>
              <span v-else>Send email</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const jobId = computed(() => route.params.id as string)

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

const job = ref<Job | null>(null)
const applications = ref<Application[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const moving = ref<string | null>(null)
const selectedApplication = ref<Application | null>(null)
const savingNotes = ref(false)
const noteSavedSuccessfully = ref<string | null>(null)

// Email functionality
const showEmailComposer = ref(false)
const sendingEmail = ref(false)
const loadingEmails = ref(false)
const emailHistory = ref<Email[]>([])
const emailTemplates = ref<EmailTemplate[]>([])
const emailForm = ref({
  subject: '',
  body: '',
  selectedTemplateId: null as number | null
})

interface EmailTemplate {
  id: number
  name: string
  subject: string
  body: string
  created_at: string
  updated_at: string
}

interface Email {
  id: number
  candidate_id: number
  subject: string
  body: string
  sender_email: string
  sender_name: string | null
  template_id: number | null
  created_at: string
}

// Structure pour stocker les notes par stage
interface StageNote {
  id: number
  application_id: string
  stage: string
  report: string
  rating: number
  interviewer?: string | null
  created_at: string
  updated_at: string
}

// Store all notes for the selected application
const applicationNotes = ref<StageNote[]>([])

// Forms pour ajouter des notes par stage
const stageNoteForms = ref<{ [key: string]: { report: string; rating: number; interviewer: string } }>({})

// Initialiser les forms pour chaque stage
const initStageNoteForms = () => {
  stages.forEach(stage => {
    if (!stageNoteForms.value[stage.key]) {
      stageNoteForms.value[stage.key] = {
        report: '',
        rating: 0,
        interviewer: ''
      }
    }
  })
}

const stages = [
  { key: 'new', label: 'New applicants' },
  { key: 'review', label: 'Screening interview' },
  { key: 'interview', label: 'Technical interview' },
  { key: 'offer', label: 'Offer sent' },
  { key: 'hired', label: 'Hired' },
  { key: 'rejected', label: 'Refused' }
]

const getApplicationsByStage = (stage: string) => {
  const filtered = applications.value.filter(app => {
    const appStage = String(app.stage).trim().toLowerCase()
    const targetStage = String(stage).trim().toLowerCase()
    return appStage === targetStage
  })
  return filtered
}

const getStageNumber = (stageKey: string) => {
  const index = stages.findIndex(s => s.key === stageKey)
  return index >= 0 ? index + 1 : '?'
}

const isCurrentStage = (appStage: string | undefined | null, stageKey: string): boolean => {
  if (!appStage) {
    console.log('isCurrentStage: appStage is falsy', { appStage, stageKey })
    return false
  }
  const appStageStr = String(appStage).trim().toLowerCase()
  const stageKeyStr = String(stageKey).trim().toLowerCase()
  const result = appStageStr === stageKeyStr
  if (result) {
    console.log('✅ Stage match found:', { appStage, stageKey, appStageStr, stageKeyStr })
  }
  return result
}

const openModal = async (app: Application) => {
  selectedApplication.value = app
  console.log('🔵 Opening modal for application:', { 
    id: app.id, 
    stage: app.stage, 
    stageType: typeof app.stage,
    stageValue: JSON.stringify(app.stage)
  })
  console.log('🔵 Available stages:', stages.map(s => ({ key: s.key, label: s.label })))
  
  // Test each stage comparison
  stages.forEach(s => {
    const isCurrent = isCurrentStage(app.stage, s.key)
    console.log(`🔵 Stage "${s.label}" (${s.key}): isCurrent=${isCurrent}, app.stage="${app.stage}"`)
  })
  
  initStageNoteForms()
  await refreshApplicationNotes()
  // Load email templates and history (non-blocking, errors are handled internally)
  loadEmailTemplates().catch(() => {}) // Ignore errors if tables don't exist yet
  refreshEmailHistory().catch(() => {}) // Ignore errors if tables don't exist yet
}

// Refresh notes for the selected application
const refreshApplicationNotes = async () => {
  if (!selectedApplication.value) {
    applicationNotes.value = []
    return
  }
  
  try {
    const notes = await $fetch<StageNote[]>(`/api/admin/applications/${selectedApplication.value.id}/notes`)
    applicationNotes.value = notes || []
    console.log(`Refreshed ${notes?.length || 0} notes for selected application`)
  } catch (err: any) {
    // Si la table n'existe pas encore, afficher un message
    if (err.statusCode === 500 || err.message?.includes('does not exist')) {
      console.error('Table application_notes does not exist. Please run the migration SQL.')
      alert('La table des notes n\'existe pas encore. Veuillez exécuter la migration SQL dans Supabase.')
    } else {
      console.error('Error fetching notes:', err)
    }
    applicationNotes.value = []
  }
}

// Get notes for a specific stage
const getStageNotes = (stageKey: string): StageNote[] => {
  return applicationNotes.value.filter(note => note.stage === stageKey)
}

// Cache for notes by application ID (for kanban display)
const notesCache = ref<{ [applicationId: string]: StageNote[] }>({})

// Fetch notes for an application (for kanban display)
const fetchNotesForApplication = async (app: Application) => {
  if (notesCache.value[app.id]) {
    return notesCache.value[app.id]
  }
  
  try {
    const notes = await $fetch<StageNote[]>(`/api/admin/applications/${app.id}/notes`)
    notesCache.value[app.id] = notes || []
    console.log(`Loaded ${notes?.length || 0} notes for application ${app.id}`)
    return notes || []
  } catch (err: any) {
    // Si la table n'existe pas encore, retourner un tableau vide
    if (err.statusCode === 500 || err.message?.includes('does not exist')) {
      console.warn(`Table application_notes might not exist yet. Please run the migration.`)
      notesCache.value[app.id] = []
      return []
    }
    console.error('Error fetching notes for application:', err)
    notesCache.value[app.id] = []
    return []
  }
}

// Get all notes for an application (for kanban display)
const getAllNotesForApplication = (app: Application): StageNote[] => {
  return notesCache.value[app.id] || []
}

// Get average rating for an application
const getAverageRating = (app: Application): number => {
  const allNotes = getAllNotesForApplication(app)
  if (allNotes.length === 0) return 0
  const sum = allNotes.reduce((acc, note) => acc + note.rating, 0)
  return sum / allNotes.length
}

// Add a note for a specific stage
const addStageNote = async (stageKey: string) => {
  if (!selectedApplication.value) return
  
  const form = stageNoteForms.value[stageKey]
  if (!form.report || !form.rating) {
    alert('Veuillez remplir le compte-rendu et sélectionner une note')
    return
  }
  
  savingNotes.value = true
  
  try {
    // Save note to backend using the new notes endpoint
    const savedNote = await $fetch(`/api/admin/applications/${selectedApplication.value.id}/notes`, {
      method: 'POST',
      body: {
        stage: stageKey,
        report: form.report.trim(),
        rating: form.rating,
        interviewer: form.interviewer?.trim() || null
      }
    })
    
    console.log('Note saved successfully:', savedNote)
    
    // Show success message
    noteSavedSuccessfully.value = stageKey
    setTimeout(() => {
      noteSavedSuccessfully.value = null
    }, 3000)
    
    // Reset form
    form.report = ''
    form.rating = 0
    form.interviewer = ''
    
    // Refresh notes for this application
    await refreshApplicationNotes()
    
    // Also refresh the cache for kanban display
    const notes = await $fetch<StageNote[]>(`/api/admin/applications/${selectedApplication.value.id}/notes`)
    notesCache.value[selectedApplication.value.id] = notes || []
    console.log('Cache updated with', notes?.length || 0, 'notes')
  } catch (err: any) {
    console.error('Error saving note:', err)
    if (err.statusCode === 500 || err.message?.includes('does not exist')) {
      alert('Erreur : La table application_notes n\'existe pas. Veuillez exécuter la migration SQL dans Supabase (voir migration_add_notes_table.sql)')
    } else {
      alert(err.data?.message || err.message || 'Erreur lors de l\'enregistrement de la note')
    }
  } finally {
    savingNotes.value = false
  }
}

const closeModal = () => {
  selectedApplication.value = null
  showEmailComposer.value = false
  emailForm.value = {
    subject: '',
    body: '',
    selectedTemplateId: null
  }
}

// Email functions
const loadEmailTemplates = async () => {
  try {
    const templates = await $fetch<EmailTemplate[]>('/api/email-templates')
    emailTemplates.value = templates || []
  } catch (err: any) {
    // Silently fail if tables don't exist yet or other errors
    console.error('Error loading email templates:', err)
    emailTemplates.value = []
  }
}

const loadTemplate = () => {
  if (emailForm.value.selectedTemplateId) {
    const template = emailTemplates.value.find(t => t.id === emailForm.value.selectedTemplateId)
    if (template) {
      emailForm.value.subject = template.subject
      emailForm.value.body = template.body
    }
  }
}

const refreshEmailHistory = async () => {
  if (!selectedApplication.value) return
  
  loadingEmails.value = true
  try {
    // candidate_id is already a UUID string
    const candidateId = selectedApplication.value.candidate_id
    const emails = await $fetch<Email[]>(`/api/candidates/${candidateId}/emails`)
    emailHistory.value = emails || []
  } catch (err: any) {
    // Silently fail if tables don't exist yet or other errors
    console.error('Error loading email history:', err)
    emailHistory.value = []
  } finally {
    loadingEmails.value = false
  }
}

const sendEmail = async () => {
  if (!selectedApplication.value || !emailForm.value.subject || !emailForm.value.body) return
  
  sendingEmail.value = true
  try {
    // candidate_id is already a UUID string
    const candidateId = selectedApplication.value.candidate_id
    
    await $fetch('/api/emails/send', {
      method: 'POST',
      body: {
        candidate_id: candidateId,
        subject: emailForm.value.subject,
        body: emailForm.value.body,
        template_id: emailForm.value.selectedTemplateId
      }
    })
    
    // Reset form and close modal
    emailForm.value = {
      subject: '',
      body: '',
      selectedTemplateId: null
    }
    showEmailComposer.value = false
    
    // Refresh email history
    await refreshEmailHistory()
    
    alert('Email envoyé avec succès!')
  } catch (err: any) {
    console.error('Error sending email:', err)
    alert(err.data?.message || err.message || 'Erreur lors de l\'envoi de l\'email')
  } finally {
    sendingEmail.value = false
  }
}

const previewEmailBody = computed(() => {
  if (!selectedApplication.value) return emailForm.value.body
  return emailForm.value.body.replace(/\{\{candidate_name\}\}/g, selectedApplication.value.candidate_name)
})

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
    
    // Update selectedApplication if it's the one being moved
    if (selectedApplication.value && selectedApplication.value.id === applicationId) {
      const updatedApp = applications.value.find(app => app.id === applicationId)
      if (updatedApp) {
        selectedApplication.value = updatedApp
        console.log('Updated selectedApplication stage:', updatedApp.stage)
      }
    }
  } catch (err: any) {
    alert(err.data?.message || err.message || 'Erreur lors du déplacement')
  } finally {
    moving.value = null
  }
}

const fetchJob = async () => {
  try {
    const data = await $fetch<Job>(`/api/admin/jobs/${jobId.value}`)
    job.value = data
  } catch (err: any) {
    console.error('Error fetching job:', err)
    // Ne pas bloquer si le job n'est pas trouvé
  }
}

const fetchApplications = async () => {
  try {
    loading.value = true
    error.value = null
    const data = await $fetch<Application[]>(`/api/admin/jobs/${jobId.value}/applications`)
    applications.value = data
    
    // Debug: log stages
    console.log('Applications loaded:', data.map(app => ({ id: app.id, stage: app.stage, stageType: typeof app.stage })))
    console.log('Available stage keys:', stages.map(s => s.key))
    
    // Pre-fetch notes for all applications
    await Promise.all(data.map(app => fetchNotesForApplication(app)))
  } catch (err: any) {
    error.value = err.data?.message || err.message || 'Erreur lors du chargement des candidatures'
  } finally {
    loading.value = false
  }
}

const handleEscape = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && selectedApplication.value) {
    closeModal()
  }
}

onMounted(() => {
  fetchJob()
  fetchApplications()
  window.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleEscape)
})
</script>

