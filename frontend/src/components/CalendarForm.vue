<template>
  <form class="container">
    <div class="row g-0 m-2">
      <div class="col-12">
        <n-input v-model:value="title" type="text" placeholder="Title" />
        <n-input v-model:value="value" type="text" placeholder="Location or Video Call" />
      </div>
    </div>
    <div class="row g-0 m-2">
      <div class="col-10">All-day</div>
      <div class="col-2"><n-switch v-model:value="disabled" /></div>
    </div>
    <div class="row g-0 m-2 justify-content-between">
      <div class="col-4">Starts</div>
      <div class="col-4 ">
        <n-date-picker v-model:value="start" type="date" value-format="yyyy-MM-dd"></n-date-picker>
      </div>
      <div class="col-4" v-if="!disabled">
        <n-time-picker use-12-hours v-model:value="time" format="h:mm a"></n-time-picker>
      </div>
    </div>
    <div class="row g-0 m-2 justify-content-between">
      <div class="col-4">Ends</div>
      <div class="col-4">
        <n-date-picker v-model:value="end" type="date"></n-date-picker>
      </div>
      <div class="col-4" v-if="!disabled">
        <n-time-picker use-12-hours v-model:value="time" format="h:mm a"></n-time-picker>
      </div>
    </div>
    <div class="row g-0 m-2">
      <div class="col-10">Repeat</div>
      <div class="col-2">
        <n-switch />
      </div>
    </div>
    <div class="row g-0 m-2">
      <div class="col-12">
        <n-input v-model:value="value" type="textarea" placeholder="Notes" />
      </div>
    </div>
  </form>
</template>

<script>
import { NDatePicker, NTimePicker, NInput, NSwitch } from "naive-ui";

export default {
  created() {},
  data() {
    return {
      value: null,
      time: null,
      disabled: null,
      // TODO: placeholders above
      title: null,
      start: null,
      end: null,
    };
  },
  props: {
    toggleSubmit: Boolean,
  },
  methods: {
    submitForm(title, start, end) {
      if (title && start) {
        this.$emit("submit", { title, start, end });
      } else {
        console.warn("Invalid submit event payload!");
      }
    },
  },
  components: {
    NDatePicker,
    NTimePicker,
    NInput,
    NSwitch,
  },
  watch: {
    toggleSubmit(val, oldVal) {
      this.submitForm(this.title, this.start, this.end);
    },
  },
  emits: {
    submit: null,
  },
};
</script>

<style scoped></style>
