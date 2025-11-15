export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const templateId = getRouterParam(event, 'id')
  
  if (!templateId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID du template manquant'
    })
  }
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/email-templates/${templateId}`, {
      method: 'DELETE',
      headers: {
        'X-API-Key': config.adminApiKey,
        'Content-Type': 'application/json'
      }
    })
    
    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.message || 'Erreur lors de la suppression du template'
    })
  }
})

