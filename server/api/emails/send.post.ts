export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  
  try {
    const response = await $fetch(`${config.public.apiBase}/api/emails/send`, {
      method: 'POST',
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
      statusMessage: error.message || 'Erreur lors de l\'envoi de l\'email'
    })
  }
})

