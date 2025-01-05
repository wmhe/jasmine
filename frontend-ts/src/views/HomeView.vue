<template>
  <div class="container d-flex flex-column h-100">
    <CalendarNavigation :title="title" v-on:open-create-event-modal="openCreateEventModal" />
    <Calendar class="flex-grow-1" :events="events" v-on:change="handleDateSetChange"
      v-on:open-create-event-modal-at-date="openCreateEventModalAtDate" />
  </div>
  <CalendarModal v-if="isCreateEventModalOpen" :initial-form-data="initialFormData" @close="closeCreateEventModal"
    @create-event="handleCreateEvent" />
</template>

<script setup lang="ts">
import CalendarModal from "@/components/CalendarModal.vue";
import CalendarNavigation from "@/components/CalendarNavigation.vue";
import { eventService } from "@/services";
import type { CalendarEvent, CreateEvent } from "@/services/api";
import { onMounted, ref } from "vue";
import Calendar from "../components/Calendar.vue";

const events = ref<CalendarEvent[]>([]);
const title = ref<string>();
const isCreateEventModalOpen = ref(false);
const initialFormData = ref<CreateEvent>(calculateFormDataNow());

function handleDateSetChange(newTitle: string) {
  title.value = newTitle;
}

function openCreateEventModal() {
  initialFormData.value = calculateFormDataNow();
  isCreateEventModalOpen.value = true;
}

function closeCreateEventModal() {
  isCreateEventModalOpen.value = false;
}

function openCreateEventModalAtDate(date: Date) {
  initialFormData.value = calculateFormDataForDate(date);
  isCreateEventModalOpen.value = true;
}

function handleCreateEvent(event: CalendarEvent) {
  closeCreateEventModal();
  events.value.push(event);
}

function calculateFormDataNow() {
  const nextHour = new Date();
  nextHour.setHours(nextHour.getHours() + 1, 0, 0, 0);
  const nextNextHour = new Date();
  nextNextHour.setHours(nextNextHour.getHours() + 2, 0, 0, 0);
  return {
    title: "",
    allDay: false,
    start: nextHour.getTime(),
    end: nextNextHour.getTime(),
  };
}

function calculateFormDataForDate(date: Date) {
  return {
    title: "",
    allDay: true,
    start: date.getTime(),
    end: date.getTime(),
  };
}

onMounted(async () => {
  events.value = await eventService.getEvents().then((res) => res.items);
});
</script>
