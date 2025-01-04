<script setup lang="ts">
import Calendar from "../components/Calendar.vue";
</script>

<template>
  <Suspense>
    <Calendar />
    <template #fallback> Loading... </template>
  </Suspense>
</template>
