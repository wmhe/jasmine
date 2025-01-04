<template>
  <div>
    <base-modal @close="closeModal" @action="toggleSubmit">
      <template #title> New Event </template>
      <template #content>
        <calendar-form
          :toggleSubmit="submitValue"
          :initial-form-data="props.initialFormData"
          @create-event="(data) => createEvent(data)"
        >
        </calendar-form>
      </template>
    </base-modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import BaseModal from "./BaseModal.vue";
import CalendarForm from "./CalendarForm.vue";
import type { CreateEvent } from "@/services/api";

interface Props {
  initialFormData: CreateEvent;
}

interface Emits {
  close: [];
  submit: [event: CreateEvent];
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

function createEvent(event: CreateEvent) {
  emit("submit", event);
}
</script>

<style scoped></style>
