import { defineEventHandler, readBody } from 'h3'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  
  const backendUrl = config.public.apiBase || 'http://127.0.0.1:8000'
  const adminApiKey = config.adminApiKey
  
  if (!adminApiKey) {
    throw createError({
      statusCode: 500,
      message: 'Admin API key not configured'
    })
  }
  
  try {
    const response = await $fetch(`${backendUrl}/api/ai/chat`, {
      method: 'POST',
      headers: {
        'X-API-Key': adminApiKey,
        'Content-Type': 'application/json'
      },
      body: {
        message: body.message
      }
    })
    
    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      message: error.data?.detail || error.message || 'Erreur lors de l\'appel à l\'assistant IA'
    })
  }
})

