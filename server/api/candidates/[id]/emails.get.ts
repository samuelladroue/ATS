export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const candidateId = getRouterParam(event, 'id')
  
  if (!candidateId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID du candidat manquant'
    })
  }
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/candidates/${candidateId}/emails`, {
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
      statusMessage: error.message || 'Erreur lors de la récupération des emails'
    })
  }
})

