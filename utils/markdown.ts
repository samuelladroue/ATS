/**
 * Utilitaire simple pour rendre du markdown basique côté client
 */
export function renderMarkdown(md: string | null | undefined): string {
  if (!md) return ''
  
  // Nettoyer les espaces en début et fin
  const cleaned = md.trim()
  
  return cleaned
    // Headers (sans marges en haut, gérées par les classes prose)
    .replace(/^### (.*$)/gim, '<h3 class="text-lg font-semibold mb-2 mt-0">$1</h3>')
    .replace(/^## (.*$)/gim, '<h2 class="text-xl font-semibold mb-3 mt-0">$1</h2>')
    .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mb-4 mt-0">$1</h1>')
    // Bold
    .replace(/\*\*(.*?)\*\*/gim, '<strong class="font-semibold">$1</strong>')
    // Italic
    .replace(/\*(.*?)\*/gim, '<em class="italic">$1</em>')
    // Links
    .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" class="text-blue-600 hover:underline" target="_blank" rel="noopener">$1</a>')
    // Line breaks (mais pas en début de ligne)
    .replace(/\n/gim, '<br />')
    // Supprimer les <br /> en début
    .replace(/^(<br \/>\s*)+/i, '')
}

