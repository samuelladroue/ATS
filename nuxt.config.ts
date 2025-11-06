// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@vueuse/nuxt'
  ],

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    // Variables privées (server-only)
    adminApiKey: process.env.NUXT_ADMIN_API_KEY || 'change-me-in-prod',
    
    // Variables publiques (exposées au client)
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000'
    }
  },

  typescript: {
    strict: true,
    typeCheck: false  // Désactivé pour éviter l'erreur vue-tsc en dev
  }
})
