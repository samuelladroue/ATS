<template>
  <div class="w-full">
    <!-- Input bar when AI Agent is closed -->
    <div v-if="!isOpen" class="w-full">
      <div class="bg-white border-2 border-primary-300 rounded-xl shadow-lg p-4 flex items-center gap-3 hover:border-primary-900 transition-all duration-200">
        <div class="flex-1">
          <input
            v-model="inputMessage"
            type="text"
            placeholder="Example: Create a designer job at 100k$ in Paris... or Create an email template to invite a candidate..."
            @keyup.enter="handleQuickSend"
            @focus="isOpen = true"
            class="w-full text-sm text-primary-900 placeholder-primary-400 focus:outline-none bg-transparent"
          />
        </div>
        <button
          @click="handleQuickSend"
          :disabled="!inputMessage.trim()"
          class="bg-primary-900 text-white rounded-lg px-4 py-2 hover:bg-primary-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center gap-2 font-medium text-sm shrink-0"
          title="Send your request"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
          <span class="hidden sm:inline">Send</span>
        </button>
      </div>
      <p class="text-xs text-primary-500 mt-2 text-center">
        AI Agent creates offers and templates from your natural language
      </p>
    </div>

    <!-- AI Agent Interface -->
    <div
      v-if="isOpen"
      class="bg-white rounded-xl shadow-lg border border-primary-200 w-full h-[500px] flex flex-col"
    >
      <!-- Header -->
      <div class="bg-primary-900 text-white px-6 py-4 rounded-t-xl flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-primary-700 rounded-full flex items-center justify-center">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-lg">🤖 AI Agent</h3>
            <p class="text-xs text-primary-300">Create jobs and templates automatically from natural language</p>
          </div>
        </div>
        <button
          @click="isOpen = false"
          class="text-primary-300 hover:text-white transition-colors p-1"
          title="Close AI Agent"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Messages -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
        <!-- Welcome message -->
        <div v-if="messages.length === 0" class="text-center text-primary-500 py-8">
          <svg class="w-12 h-12 mx-auto mb-4 text-primary-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          <p class="text-sm font-semibold mb-4 text-primary-900">🤖 AI Agent</p>
          <div class="bg-primary-50 border border-primary-200 rounded-lg p-4 max-w-md mx-auto text-left">
            <p class="text-xs font-medium text-primary-900 mb-2">Examples:</p>
            <ul class="text-xs text-primary-600 space-y-1">
              <li>• "Create a designer job at 80k€ in Lyon"</li>
              <li>• "Email template to invite for an interview"</li>
            </ul>
          </div>
        </div>

        <!-- Message list -->
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="[
            'flex',
            message.role === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            :class="[
              'max-w-[80%] rounded-2xl px-4 py-3',
              message.role === 'user'
                ? 'bg-primary-900 text-white'
                : 'bg-primary-50 text-primary-900 border border-primary-200'
            ]"
          >
            <div class="text-sm whitespace-pre-wrap">{{ message.content }}</div>
            <div
              v-if="message.jobCreated"
              class="mt-3 pt-3 border-t border-primary-200"
            >
              <div class="text-xs font-semibold mb-2">Job created:</div>
              <NuxtLink
                :to="`/admin/jobs/${message.jobCreated.id}`"
                class="text-xs text-primary-600 hover:text-primary-900 hover:underline font-medium"
              >
                {{ message.jobCreated.title }}
              </NuxtLink>
            </div>
            <div
              v-if="message.templateCreated"
              class="mt-3 pt-3 border-t border-primary-200"
            >
              <div class="text-xs font-semibold mb-2">Template created:</div>
              <NuxtLink
                :to="`/admin/email-templates`"
                class="text-xs text-primary-600 hover:text-primary-900 hover:underline font-medium"
              >
                {{ message.templateCreated.name }}
              </NuxtLink>
              <div class="text-xs text-primary-500 mt-1">Subject: {{ message.templateCreated.subject }}</div>
            </div>
            <div class="text-xs opacity-70 mt-2">
              {{ formatTime(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="loading" class="flex justify-start">
          <div class="bg-primary-50 border border-primary-200 rounded-2xl px-4 py-3">
            <div class="flex items-center gap-2">
              <div class="animate-spin rounded-full h-4 w-4 border-2 border-primary-300 border-t-primary-900"></div>
              <span class="text-sm text-primary-600">Agent is processing your request...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="border-t border-primary-200 p-4">
        <form @submit.prevent="sendMessage" class="flex gap-2">
          <input
            v-model="inputMessage"
            type="text"
            placeholder="Type your message..."
            :disabled="loading"
            class="flex-1 px-4 py-2 border border-primary-300 rounded-xl focus:ring-2 focus:ring-primary-900 focus:border-primary-900 bg-white text-primary-900 placeholder-primary-400 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            :disabled="loading || !inputMessage.trim()"
            class="bg-primary-900 text-white px-6 py-2 rounded-xl font-medium hover:bg-primary-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <svg v-if="!loading" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
            <div v-else class="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  jobCreated?: {
    id: string
    title: string
    slug: string
  }
  templateCreated?: {
    id: number
    name: string
    subject: string
  }
}

const isOpen = ref(false)
const inputMessage = ref('')
const messages = ref<Message[]>([])
const loading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const handleQuickSend = async () => {
  if (!inputMessage.value.trim()) return
  // Open AI Agent if closed
  if (!isOpen.value) {
    isOpen.value = true
    await nextTick()
  }
  await sendMessage()
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  // Add user message
  messages.value.push({
    role: 'user',
    content: userMessage,
    timestamp: new Date()
  })

  // Scroll to bottom
  await nextTick()
  scrollToBottom()

  // Send to API
  loading.value = true
  try {
    const response = await $fetch<{
      response: string
      job_created?: {
        id: string
        title: string
        slug: string
      }
      template_created?: {
        id: number
        name: string
        subject: string
      }
      error?: string
    }>('/api/ai/chat', {
      method: 'POST',
      body: {
        message: userMessage
      }
    })

    // Add assistant response
    messages.value.push({
      role: 'assistant',
      content: response.response,
      timestamp: new Date(),
      jobCreated: response.job_created ? {
        id: response.job_created.id,
        title: response.job_created.title,
        slug: response.job_created.slug
      } : undefined,
      templateCreated: response.template_created ? {
        id: response.template_created.id,
        name: response.template_created.name,
        subject: response.template_created.subject
      } : undefined
    })

    // Scroll to bottom
    await nextTick()
    scrollToBottom()
  } catch (error: any) {
    messages.value.push({
      role: 'assistant',
      content: `❌ Erreur : ${error.data?.message || error.message || 'Une erreur est survenue'}`,
      timestamp: new Date()
    })
    await nextTick()
    scrollToBottom()
  } finally {
    loading.value = false
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Auto-scroll when new messages arrive
watch(messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })
</script>

