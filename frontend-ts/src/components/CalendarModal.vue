<template>
  <div>
    <BaseModal @close="closeModal" @action="toggleSubmit">
      <template #title> New Event </template>
      <template #content>
        <CalendarForm
          :toggle-submit="submitValue"
          :initial-form-data="props.initialFormData"
          @create-event="handleCreateEvent"
        />
      </template>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import BaseModal from "./BaseModal.vue";
import CalendarForm from "./CalendarForm.vue";
import type { CreateEvent, CalendarEvent } from "@/services/api";

interface Props {
  initialFormData: CreateEvent;
}

interface Emits {
  close: [];
  createEvent: [event: CalendarEvent];
}

const props = defineProps<Props>();

const emit = defineEmits<Emits>();

const submitValue = ref(false);

function closeModal() {
  emit("close");
}

// TODO: This can probably be done in a more concise way.
function toggleSubmit() {
  submitValue.value = !submitValue.value;
}

function handleCreateEvent(event: CalendarEvent) {
  emit("createEvent", event);
}
</script>

<style scoped></style>
