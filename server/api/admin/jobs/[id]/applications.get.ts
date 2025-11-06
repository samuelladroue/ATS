export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const jobId = getRouterParam(event, 'id')
  
  if (!jobId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID de l\'offre manquant'
    })
  }
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/jobs/${jobId}/applications`, {
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
      statusMessage: error.message || 'Erreur lors de la récupération des candidatures'
    })
  }
})

