<script lang="ts">
import { defineComponent, type PropType } from "vue";
import BaseModal from "./BaseModal.vue";
import CalendarForm from "./CalendarForm.vue";

interface FormData {
  title: string
  start: number
  end: number
  allDay: boolean
}

export default defineComponent({
  created() {},
  data() {
    return {
      submitValue: false,
    };
  },
  props: {
    initialFormData: {
      type: Object as PropType<FormData>,
        required: true
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    toggleSubmit() {
      this.submitValue = !this.submitValue;
    },
    submitForm(data: object) {
      this.$emit("submit", data);
    },
  },
  components: {
    BaseModal,
    CalendarForm,
  },
  emits: {
    close: null,
    submit: null,
  },
})
</script>

<template>
  <div>
    <BaseModal @close="closeModal" @action="toggleSubmit">
      <template #title> New Event </template>
      <template #content>
        <CalendarForm
          :toggleSubmit="submitValue"
          :initial-form-data="initialFormData"
          @submit="submitForm"
        ></CalendarForm>
      </template>
    </BaseModal>
  </div>
</template>

<style scoped></style>
