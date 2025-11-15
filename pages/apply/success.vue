<template>
  <div class="min-h-screen bg-white flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full bg-white rounded-2xl border border-primary-200 p-8 sm:p-10 text-center">
      <div class="mb-8">
        <div class="mx-auto flex items-center justify-center h-20 w-20 rounded-full bg-primary-100 border-2 border-primary-200">
          <svg class="h-10 w-10 text-primary-900" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
        </div>
      </div>

      <h1 class="text-3xl sm:text-4xl font-semibold text-primary-900 mb-4 tracking-tight">
        Candidature envoyée !
      </h1>

      <p class="text-primary-700 mb-3 text-lg">
        Merci pour votre candidature{{ jobTitle ? ` pour le poste de ${jobTitle}` : '' }}.
      </p>

      <p class="text-sm text-primary-600 mb-10 leading-relaxed">
        Nous avons bien reçu votre candidature et allons l'examiner dans les plus brefs délais.
      </p>

      <div class="space-y-3">
        <NuxtLink
          to="/"
          class="block w-full bg-primary-900 text-white py-3.5 px-6 rounded-xl font-medium hover:bg-primary-800 transition-all duration-200 text-sm"
        >
          Voir d'autres offres
        </NuxtLink>
        
        <NuxtLink
          to="/"
          class="block w-full bg-white border border-primary-300 text-primary-900 py-3.5 px-6 rounded-xl font-medium hover:bg-primary-50 transition-all duration-200 text-sm"
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

