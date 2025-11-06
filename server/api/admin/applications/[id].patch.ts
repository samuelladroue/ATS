export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const applicationId = getRouterParam(event, 'id')
  const body = await readBody(event)
  
  if (!applicationId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID de la candidature manquant'
    })
  }
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/applications/${applicationId}`, {
      method: 'PATCH',
      headers: {
        'X-API-Key': config.adminApiKey,
        'Content-Type': 'application/json'
      },
      body
    })
    
    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.message || 'Erreur lors de la mise à jour de la candidature'
    })
  }
})

