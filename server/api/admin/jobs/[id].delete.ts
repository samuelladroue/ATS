import { defineEventHandler, getRouterParam } from 'h3'
import { useRuntimeConfig } from '#imports'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const jobId = getRouterParam(event, 'id')

  if (!jobId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Job ID is required',
    })
  }

  try {
    const response = await $fetch(`${config.public.apiBase}/api/jobs/${jobId}`, {
      method: 'DELETE',
      headers: {
        'x-api-key': config.adminApiKey,
      },
    })

    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.statusMessage || 'Erreur lors de la suppression de l\'offre',
      data: error.data || error.message,
    })
  }
})

