<template>
  <div>
    <NavigationBar />
    <NuxtPage />
  </div>
</template>

<script setup>
useHead({
  script: [
    {
      src: 'https://cdn.tailwindcss.com',
      tagPosition: 'head'
    }
  ]
})
</script>

