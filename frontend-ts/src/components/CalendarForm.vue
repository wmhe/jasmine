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
          v-model:value="startTime"
          format="h:mm a"
          use-12-hours
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
          v-model:value="endTime"
          format="h:mm a"
          use-12-hours
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

<script setup lang="ts">
import type { Event } from "@/services/api";
import { NDatePicker, NInput, NSwitch, NTimePicker } from "naive-ui";
import { onMounted, ref, useTemplateRef, watch } from "vue";

interface Props {
  toggleSubmit: boolean;
  initialFormData: Event;
}

interface Emits {
  addEvent: [event: Event];
}

type NInputType = InstanceType<typeof NInput>;

const props = defineProps<Props>();

const emit = defineEmits<Emits>();

const title = ref<string>();
const allDay = ref(props.initialFormData.allDay);
const start = ref(props.initialFormData.start);
const startTime = ref(props.initialFormData.start);
const end = ref(props.initialFormData.end);
const endTime = ref(props.initialFormData.end);
const inputRef = useTemplateRef<NInputType>("autofocus");

async function addEvent(title: string, start: number, end: number) {
  if (title && start) {
    emit("addEvent", {
      title,
      start,
      end,
      allDay: false,
    });
  }
}

watch(
  () => props.toggleSubmit,
  () => {
    if (title.value) {
      addEvent(title.value, start.value, end.value);
    }
  }
);

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<style scoped></style>
