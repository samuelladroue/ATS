export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const templateId = getRouterParam(event, 'id')
  const body = await readBody(event)
  
  if (!templateId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID du template manquant'
    })
  }
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/email-templates/${templateId}`, {
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
      statusMessage: error.message || 'Erreur lors de la mise à jour du template'
    })
  }
})

