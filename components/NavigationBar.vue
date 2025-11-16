<template>
  <nav class="sticky top-0 z-50 bg-white border-b border-primary-200 backdrop-blur-sm bg-opacity-95">
    <div class="max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
      <div class="flex items-center justify-between h-16">
        <!-- Logo / Brand -->
        <NuxtLink to="/" class="flex items-center gap-2 group">
          <h1 class="text-xl font-semibold text-primary-900 tracking-tight group-hover:text-primary-700 transition-colors">
            Netter ATS
          </h1>
        </NuxtLink>

        <!-- Space Switcher -->
        <div class="flex items-center gap-2 bg-primary-50 rounded-xl p-1 border border-primary-200">
          <NuxtLink
            to="/"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
              isCandidateSpace
                ? 'bg-white text-primary-900 border-2 border-primary-900'
                : 'text-primary-600 hover:text-primary-900'
            ]"
          >
            Candidate
          </NuxtLink>
          <NuxtLink
            to="/admin/jobs"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
              isAdminSpace
                ? 'bg-white text-primary-900 border-2 border-primary-900'
                : 'text-primary-600 hover:text-primary-900'
            ]"
          >
            Admin
          </NuxtLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
const route = useRoute()

const isCandidateSpace = computed(() => {
  return !route.path.startsWith('/admin')
})

const isAdminSpace = computed(() => {
  return route.path.startsWith('/admin')
})
</script>

