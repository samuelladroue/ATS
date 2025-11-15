export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/email-templates`, {
      method: 'GET',
      headers: {
        'X-API-Key': config.adminApiKey,
        'Content-Type': 'application/json'
      }
    })
    
    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.message || 'Erreur lors de la récupération des templates'
    })
  }
})

