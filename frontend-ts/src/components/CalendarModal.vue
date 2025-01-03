<template>
  <div>
    <BaseModal @close="closeModal" @action="toggleSubmit">
      <template #title> New Event </template>
      <template #content>
        <CalendarForm
          :toggleSubmit="submitValue"
          :initial-form-data="props.initialFormData"
          @submit="submitForm"
        ></CalendarForm>
      </template>
    </BaseModal>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import BaseModal from "./BaseModal.vue";
import CalendarForm from "./CalendarForm.vue";

interface EventFormData {
  title: string;
  start: number;
  end: number;
  allDay: boolean;
}

interface Props {
  initialFormData: EventFormData;
}

const props = defineProps<Props>();

const emit = defineEmits(["close", "submit"]);

const submitValue = ref(false);

function closeModal() {
  emit("close");
}

function toggleSubmit() {
  submitValue.value = !submitValue.value;
}

function submitForm(data: EventFormData) {
  emit("submit", data);
}
</script>

<style scoped></style>
