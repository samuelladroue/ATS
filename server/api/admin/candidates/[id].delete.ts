import { defineEventHandler, getRouterParam } from 'h3'
import { useRuntimeConfig } from '#imports'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const candidateId = getRouterParam(event, 'id')

  if (!candidateId) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Candidate ID is required',
    })
  }

  try {
    const response = await $fetch(`${config.public.apiBase}/api/candidates/${candidateId}`, {
      method: 'DELETE',
      headers: {
        'x-api-key': config.adminApiKey,
      },
    })

    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.statusMessage || 'Erreur lors de la suppression du candidat',
      data: error.data || error.message,
    })
  }
})

