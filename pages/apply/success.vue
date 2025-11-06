<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
      <div class="mb-6">
        <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-green-100">
          <svg class="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
      </div>

      <h1 class="text-2xl font-bold text-gray-900 mb-4">
        Candidature envoyée !
      </h1>

      <p class="text-gray-600 mb-2">
        Merci pour votre candidature{{ jobTitle ? ` pour le poste de ${jobTitle}` : '' }}.
      </p>

      <p class="text-sm text-gray-500 mb-8">
        Nous avons bien reçu votre candidature et allons l'examiner dans les plus brefs délais.
      </p>

      <div class="space-y-3">
        <NuxtLink
          to="/jobs/public"
          class="block w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          Voir d'autres offres
        </NuxtLink>
        
        <NuxtLink
          to="/"
          class="block w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors"
        >
          Retour à l'accueil
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const jobTitle = computed(() => {
  const job = route.query.job
  return typeof job === 'string' ? job : null
})
</script>

