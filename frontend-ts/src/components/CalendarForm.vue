<template>
  <div class="container">
    <div class="row g-0 m-2">
      <NInput
        v-model:value="title"
        type="text"
        placeholder="Title"
        ref="autofocus"
        class="col-12"
      />
      <NInput type="text" placeholder="Location or Video Call" class="col-12" />
    </div>
    <div class="row g-0 m-2">
      <div class="col-10">All-day</div>
      <NSwitch v-model:value="allDay" :default-value="allDay" class="col-2" />
    </div>
    <div class="row g-0 m-2 justify-content-between">
      <div class="col-4">Starts</div>
      <NDatePicker
        v-model:value="start"
        type="date"
        :default-value="start"
        class="col-4"
      />
      <NTimePicker
        v-if="!allDay"
        v-model:value="startTime"
        format="h:mm a"
        use-12-hours
        :default-value="startTime"
        class="col-4"
      />
    </div>
    <div class="row g-0 m-2 justify-content-between">
      <div class="col-4">Ends</div>
      <NDatePicker v-model:value="end" type="date" :default-value="end" class="col-4" />
      <NTimePicker
        v-if="!allDay"
        v-model:value="endTime"
        format="h:mm a"
        use-12-hours
        :default-value="endTime"
        class="col-4"
      />
    </div>
    <div class="row g-0 m-2">
      <div class="col-10">Repeat</div>
      <NSwitch class="col-2" />
    </div>
    <div class="row g-0 m-2">
      <NInput type="textarea" placeholder="Notes" class="col-12" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { eventService } from "@/services";
import type { CreateEvent, CalendarEvent } from "@/services/api";
import { NDatePicker, NInput, NSwitch, NTimePicker } from "naive-ui";
import { onMounted, ref, useTemplateRef, watch } from "vue";

interface Props {
  toggleSubmit: boolean;
  initialFormData: CreateEvent;
}

interface Emits {
  createEvent: [event: CalendarEvent];
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

async function submitEvent() {
  if (title.value && start.value) {
    const newEvent = await eventService.createEvent({
      title: title.value,
      start: start.value,
      allDay: allDay.value,
      end: end.value,
    });
    emit("createEvent", newEvent);
  }
}

watch(() => props.toggleSubmit, submitEvent, { immediate: true });

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<style scoped></style>
