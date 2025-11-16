<template>
  <div class="min-h-screen bg-white py-8 sm:py-12">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <!-- Admin Navigation (includes AI Agent) -->
      <AdminNavigation />
      
      <!-- Header -->
      <div class="mb-10">
        <div class="flex items-start justify-between flex-wrap gap-6">
          <div class="flex-1">
            <h1 class="text-4xl sm:text-5xl font-semibold text-primary-900 mb-3 tracking-tight">Email Templates</h1>
            <p class="text-primary-600 text-lg">Create and manage your email templates to communicate with candidates</p>
          </div>
          <button
            @click="showCreateForm = !showCreateForm"
            class="w-full mb-3 inline-flex items-center justify-center border-2 border-primary-900 text-primary-900 py-2 px-4 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-sm whitespace-nowrap shrink-0"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" :d="showCreateForm ? 'M6 18L18 6M6 6l12 12' : 'M12 4v16m8-8H4'" />
            </svg>
            {{ showCreateForm ? 'Hide form' : 'Create template' }}
          </button>
        </div>
      </div>

      <!-- Create Template Form -->
      <div v-if="showCreateForm" class="bg-white rounded-2xl border border-primary-200 p-6 sm:p-8 mb-10">
        <h2 class="text-2xl font-semibold mb-6 text-primary-900">
          {{ editingTemplate ? 'Edit template' : 'Create new template' }}
        </h2>
        
        <form @submit.prevent="saveTemplate" class="space-y-5">
          <div>
            <label for="template-name" class="block text-sm font-medium text-primary-900 mb-2">
              Template name *
            </label>
            <input
              id="template-name"
              v-model="templateForm.name"
              type="text"
              required
              class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400"
              placeholder="Ex: Technical interview invitation"
            />
          </div>

          <div>
            <label for="template-subject" class="block text-sm font-medium text-primary-900 mb-2">
              Subject *
            </label>
            <input
              id="template-subject"
              v-model="templateForm.subject"
              type="text"
              required
              class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400"
              placeholder="Ex: Invitation to a technical interview"
            />
            <p class="text-xs text-primary-500 mt-2">
              You can use <code class="bg-primary-100 px-1 rounded">{{candidate_name}}</code> to insert the candidate's name
            </p>
          </div>

          <div>
            <label for="template-body" class="block text-sm font-medium text-primary-900 mb-2">
              Message body *
            </label>
            <textarea
              id="template-body"
              v-model="templateForm.body"
              rows="10"
              required
              class="w-full px-4 py-3 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 resize-none"
              placeholder="Email body..."
            ></textarea>
            <p class="text-xs text-primary-500 mt-2">
              You can use <code class="bg-primary-100 px-1 rounded">{{candidate_name}}</code> to insert the candidate's name
            </p>
          </div>

          <!-- Preview -->
          <div v-if="templateForm.subject || templateForm.body" class="bg-primary-50 rounded-xl p-4 border border-primary-200">
            <p class="text-xs font-medium text-primary-700 mb-2">Preview:</p>
            <p class="text-sm font-semibold text-primary-900 mb-2">{{ templateForm.subject || '(No subject)' }}</p>
            <div class="text-sm text-primary-700 whitespace-pre-wrap">{{ templateForm.body }}</div>
          </div>

          <div class="flex gap-3 pt-4">
            <button
              type="button"
              @click="cancelEdit"
              class="flex-1 px-4 py-3 border-2 border-primary-900 text-primary-900 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 bg-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="savingTemplate"
              :class="[
                'flex-1 px-4 py-3 border-2 border-primary-900 rounded-xl font-medium transition-all duration-200',
                savingTemplate
                  ? 'bg-primary-200 text-primary-500 cursor-not-allowed border-primary-300'
                  : 'bg-white text-primary-900 hover:bg-primary-900 hover:text-white'
              ]"
            >
              <span v-if="savingTemplate">Saving...</span>
              <span v-else>{{ editingTemplate ? 'Update' : 'Create template' }}</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Templates List -->
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-10 w-10 border-2 border-primary-200 border-t-primary-900"></div>
        <p class="mt-6 text-primary-600 text-sm">Loading templates...</p>
      </div>

      <div v-else-if="error" class="bg-primary-50 border border-primary-200 rounded-xl p-6 text-center max-w-md mx-auto">
        <p class="text-primary-700 text-sm">{{ error }}</p>
      </div>

      <div v-else-if="templates.length === 0" class="text-center py-20">
        <p class="text-primary-600 mb-6">No templates created yet.</p>
        <button
          @click="showCreateForm = true"
          class="w-full mb-3 inline-flex items-center justify-center border-2 border-primary-900 text-primary-900 py-2 px-4 rounded-xl font-medium hover:bg-primary-900 hover:text-white transition-all duration-200 text-sm"
        >
          Create your first template
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="template in templates"
          :key="template.id"
          class="bg-white rounded-2xl border-2 border-primary-200 p-6 hover:border-primary-900 transition-all duration-200"
        >
          <div class="flex items-start justify-between mb-4">
            <h3 class="text-lg font-semibold text-primary-900">{{ template.name }}</h3>
            <div class="flex gap-2">
              <button
                @click="editTemplate(template)"
                class="text-primary-600 hover:text-primary-900 transition-colors"
                title="Edit"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                @click="confirmDeleteTemplate(template)"
                class="text-red-600 hover:text-red-900 transition-colors"
                title="Delete"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="space-y-3">
            <div>
              <p class="text-xs font-medium text-primary-500 mb-1">Subject:</p>
              <p class="text-sm text-primary-900">{{ template.subject }}</p>
            </div>
            <div>
              <p class="text-xs font-medium text-primary-500 mb-1">Body:</p>
              <p class="text-sm text-primary-700 line-clamp-3">{{ template.body }}</p>
            </div>
            <div class="pt-3 border-t border-primary-200">
              <p class="text-xs text-primary-500">
                Created on {{ formatDate(template.created_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface EmailTemplate {
  id: number
  name: string
  subject: string
  body: string
  created_at: string
  updated_at: string
}

const templates = ref<EmailTemplate[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const showCreateForm = ref(false)
const savingTemplate = ref(false)
const editingTemplate = ref<EmailTemplate | null>(null)
const templateForm = ref({
  name: '',
  subject: '',
  body: ''
})

const loadTemplates = async () => {
  try {
    loading.value = true
    error.value = null
    const data = await $fetch<EmailTemplate[]>('/api/email-templates')
    templates.value = data || []
  } catch (err: any) {
    error.value = err.data?.message || err.message || 'Error loading templates'
  } finally {
    loading.value = false
  }
}

const saveTemplate = async () => {
  if (!templateForm.value.name || !templateForm.value.subject || !templateForm.value.body) return
  
  savingTemplate.value = true
  try {
    if (editingTemplate.value) {
      // Update existing template
      await $fetch(`/api/email-templates/${editingTemplate.value.id}`, {
        method: 'PATCH',
        body: {
          name: templateForm.value.name,
          subject: templateForm.value.subject,
          body: templateForm.value.body
        }
      })
    } else {
      // Create new template
      await $fetch('/api/email-templates', {
        method: 'POST',
        body: {
          name: templateForm.value.name,
          subject: templateForm.value.subject,
          body: templateForm.value.body
        }
      })
    }
    
    // Reset form
    templateForm.value = {
      name: '',
      subject: '',
      body: ''
    }
    editingTemplate.value = null
    showCreateForm.value = false
    
    // Reload templates
    await loadTemplates()
  } catch (err: any) {
    alert(err.data?.message || err.message || 'Error saving template')
  } finally {
    savingTemplate.value = false
  }
}

const editTemplate = (template: EmailTemplate) => {
  editingTemplate.value = template
  templateForm.value = {
    name: template.name,
    subject: template.subject,
    body: template.body
  }
  showCreateForm.value = true
  // Scroll to form
  setTimeout(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }, 100)
}

const cancelEdit = () => {
  editingTemplate.value = null
  templateForm.value = {
    name: '',
    subject: '',
    body: ''
  }
  showCreateForm.value = false
}

const confirmDeleteTemplate = (template: EmailTemplate) => {
  if (confirm(`Are you sure you want to delete the template "${template.name}"?`)) {
    deleteTemplate(template.id)
  }
}

const deleteTemplate = async (templateId: number) => {
  try {
    await $fetch(`/api/email-templates/${templateId}`, {
      method: 'DELETE'
    })
    
    // Reload templates
    await loadTemplates()
  } catch (err: any) {
    alert(err.data?.message || err.message || 'Error deleting template')
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  loadTemplates()
})
</script>

