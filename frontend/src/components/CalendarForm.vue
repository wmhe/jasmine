<template>
  <form class="container">
    <div class="row g-0 m-2">
      <div class="col-12">
        <n-input v-model:value="title" type="text" placeholder="Title" ref="autofocus" />
        <n-input type="text" placeholder="Location or Video Call" />
      </div>
    </div>
    <div class="row g-0 m-2">
      <div class="col-10">All-day</div>
      <div class="col-2"><n-switch v-model:value="allDay" :default-value="allDay" /></div>
    </div>
    <div class="row g-0 m-2 justify-content-between">
      <div class="col-4">Starts</div>
      <div class="col-4">
        <n-date-picker
          v-model:value="start"
          type="date"
          :default-value="start"
        ></n-date-picker>
      </div>
      <div class="col-4" v-if="!allDay">
        <n-time-picker
          use-12-hours
          v-model:value="startTime"
          format="h:mm a"
          :default-value="startTime"
        ></n-time-picker>
      </div>
    </div>
    <div class="row g-0 m-2 justify-content-between">
      <div class="col-4">Ends</div>
      <div class="col-4">
        <n-date-picker
          v-model:value="end"
          type="date"
          :default-value="end"
        ></n-date-picker>
      </div>
      <div class="col-4" v-if="!allDay">
        <n-time-picker
          use-12-hours
          v-model:value="endTime"
          format="h:mm a"
          :default-value="endTime"
        ></n-time-picker>
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
        <n-input type="textarea" placeholder="Notes" />
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
      title: null,
      allDay: this.initialFormData.allDay,
      start: this.initialFormData.start,
      startTime: this.initialFormData.start,
      end: this.initialFormData.end,
      endTime: this.initialFormData.end,
    };
  },
  props: {
    toggleSubmit: Boolean,
    initialFormData: Object,
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
  mounted() {
    this.$nextTick(() => {
      this.$refs.autofocus.focus();
    });
  },
};
</script>

<style scoped></style>
