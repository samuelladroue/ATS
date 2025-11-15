import { defineEventHandler } from 'h3'
import { useRuntimeConfig } from '#imports'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const apiKey = config.adminApiKey

  try {
    const response = await $fetch(`${config.public.apiBase}/api/candidates`, {
      headers: {
        'x-api-key': apiKey,
      },
    })

    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.statusMessage || 'Erreur lors du chargement des candidats',
      data: error.data || error.message,
    })
  }
})

