export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const applicationId = getRouterParam(event, 'id')
  
  if (!applicationId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID de la candidature manquant'
    })
  }
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/applications/${applicationId}/notes`, {
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
      statusMessage: error.message || 'Erreur lors de la récupération des notes'
    })
  }
})

