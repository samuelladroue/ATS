export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const applicationId = getRouterParam(event, 'id')
  const body = await readBody(event)
  
  console.log('POST /api/admin/applications/[id]/notes - applicationId:', applicationId)
  console.log('Body:', body)
  
  if (!applicationId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID de la candidature manquant'
    })
  }
  
  const backendUrl = `${config.public.apiBase}/api/applications/${applicationId}/notes`
  console.log('Calling backend:', backendUrl)
  
  try {
    const response = await $fetch(backendUrl, {
      method: 'POST',
      headers: {
        'X-API-Key': config.adminApiKey,
        'Content-Type': 'application/json'
      },
      body
    })
    
    console.log('Backend response:', response)
    return response
  } catch (error: any) {
    console.error('Error calling backend:', error)
    console.error('Error details:', {
      statusCode: error.statusCode,
      statusMessage: error.statusMessage,
      message: error.message,
      data: error.data
    })
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.message || error.statusMessage || 'Erreur lors de la création de la note',
      data: error.data
    })
  }
})

