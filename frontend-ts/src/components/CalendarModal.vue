<template>
  <div>
    <base-modal @close="closeModal" @action="toggleSubmit">
      <template #title> New Event </template>
      <template #content>
        <calendar-form
          :toggleSubmit="submitValue"
          :initial-form-data="props.initialFormData"
          @add-event="(data) => addEvent(data)"
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
import type { Event } from "@/services/api";

interface Props {
  initialFormData: Event;
}

interface Emits {
  close: [];
  submit: [event: Event];
}

const props = defineProps<Props>();

const emit = defineEmits<Emits>();

const submitValue = ref(false);

function closeModal() {
  emit("close");
}

function toggleSubmit() {
  submitValue.value = !submitValue.value;
}

function addEvent(event: Event) {
  emit("submit", event);
}
</script>

<style scoped></style>
