<template>
  <AppNavigation>
    <div class="d-flex justify-content-between">
      <div class="p-2 text-secondary">{{ props.title }}</div>
      <div class="d-flex justify-content-end">
        <div class="p-2" role="button"><i class="bi bi-0-circle text-secondary"></i></div>
        <div class="p-2" role="button"><i class="bi bi-search text-secondary"></i></div>
        <div class="p-2" role="button" @click="emit('openCreateEventModal')">
          <i class="bi bi-plus-lg text-secondary"></i>
        </div>
      </div>
    </div>
  </AppNavigation>
</template>

<script setup lang="ts">
import AppNavigation from "./AppNavigation.vue";

interface Props {
  title?: string;
}
interface Emits {
  openCreateEventModal: [];
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<style lang="scss" scoped></style>
