<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="container-fluid h-100 p-0" ref="target">
    <div class="row h-100">
      <div class="d-flex h-100">
        <!-- @vue-expect-error options undefined-->
        <full-calendar ref="fullCalendar" :options="calendarOptions"></full-calendar>
      </div>
    </div>
  </div>
  <div>
    <calendar-modal
      v-if="isModalOpen"
      :initial-form-data="formData"
      @close="() => (isModalOpen = false)"
      @submit="(data) => submitForm(data)"
    ></calendar-modal>
  </div>
</template>

<script setup lang="ts">
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import FullCalendar from "@fullcalendar/vue3";
import { ref, useTemplateRef } from "vue";
import CalendarModal from "./CalendarModal.vue";
import type { CreateEvent, Event } from "@/services/api";
import { usePointerSwipe } from "@vueuse/core";
import { eventService } from "@/services";

type FullCalendarType = InstanceType<typeof FullCalendar>;

const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: "dayGridMonth",
  weekNumbers: true,
  customButtons: {
    menu: {
      icon: "bi bi-list fs-1 text-primary",
    },
    create: {
      icon: "bi bi-plus fs-1 text-primary",
      click: handleNewEvent,
    },
    search: {
      icon: "bi bi-search fs-1 text-primary",
    },
    customToday: {
      icon: "bi bi-0-circle fs-1 text-primary",
    },
  },
  headerToolbar: {
    start: "menu title",
    center: "",
    end: "customToday search create",
  },
  titleFormat: {
    month: "short",
  },
  dayHeaderFormat: {
    weekday: "narrow",
  },
  themeSystem: "bootstrap5",
  dateClick: handleDateClick,
  events: <Event[]>[],
});

const isModalOpen = ref(false);
const pointerdownTimestamp = ref(Date.now());
const formData = ref(calculateFormDataNow());
const calendarRef = useTemplateRef<FullCalendarType>("fullCalendar");

const target = ref<HTMLElement | null>(null);

usePointerSwipe(target, {
  onSwipeEnd(e, direction) {
    if (direction == "left") {
      calendarRef.value?.getApi().next();
    } else if (direction == "right") {
      calendarRef.value?.getApi().prev();
    }
  },
});

function handleNewEvent() {
  formData.value = calculateFormDataNow();
  isModalOpen.value = true;
}

function handleDateClick(info: { date: Date }) {
  const offset = Date.now() - pointerdownTimestamp.value;
  if (offset > 5000) {
    formData.value = calculateFormDataForDate(info.date);
    isModalOpen.value = true;
  }
}

async function submitForm(data: CreateEvent) {
  await eventService
    .createEvent(data)
    .then((event) => {
      calendarOptions.value.events.push(event);
      isModalOpen.value = false;
    })
    .catch((error) => {
      console.log(error);
    });
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

calendarOptions.value.events = await eventService.getEvents().then((res) => res.items);
</script>

<style scoped></style>
