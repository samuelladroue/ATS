<template>
  <nav class="bg-white border-b border-primary-200 mb-8">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <!-- AI Chatbox Section -->
      <div class="py-4 mb-4">
        <AIChatbox />
      </div>
      
      <!-- Navigation Links -->
      <div class="flex items-center gap-6 py-4 border-t border-primary-100">
        <NuxtLink
          to="/admin/jobs"
          :class="[
            'text-sm font-medium transition-all duration-200 pb-2 border-b-2',
            isActive('/admin/jobs')
              ? 'text-primary-900 border-primary-900'
              : 'text-primary-600 border-transparent hover:text-primary-900 hover:border-primary-300'
          ]"
        >
          Jobs
        </NuxtLink>
        <NuxtLink
          to="/admin/candidates"
          :class="[
            'text-sm font-medium transition-all duration-200 pb-2 border-b-2',
            isActive('/admin/candidates')
              ? 'text-primary-900 border-primary-900'
              : 'text-primary-600 border-transparent hover:text-primary-900 hover:border-primary-300'
          ]"
        >
          Candidates
        </NuxtLink>
        <NuxtLink
          to="/admin/email-templates"
          :class="[
            'text-sm font-medium transition-all duration-200 pb-2 border-b-2',
            isActive('/admin/email-templates')
              ? 'text-primary-900 border-primary-900'
              : 'text-primary-600 border-transparent hover:text-primary-900 hover:border-primary-300'
          ]"
        >
          Templates
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
const route = useRoute()

const isActive = (path: string) => {
  if (path === '/admin/jobs') {
    return route.path.startsWith('/admin/jobs') && route.path !== '/admin/candidates' && route.path !== '/admin/email-templates'
  }
  return route.path === path
}
</script>


