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

<script>
import BaseModal from "./BaseModal.vue";
import CalendarForm from "./CalendarForm.vue";

export default {
  created() {},
  data() {
    return {
      submitValue: false,
    };
  },
  props: {
    initialFormData: Object,
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    toggleSubmit() {
      this.submitValue = !this.submitValue;
    },
    submitForm(data) {
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
};
</script>

<style scoped></style>
