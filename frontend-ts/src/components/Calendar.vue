<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="container-fluid h-100 p-0">
    <div class="row h-100">
      <FullCalendar ref="fullCalendar" :options="calendarOptions" class="d-flex h-100" />
    </div>
  </div>
  <CalendarModal
    v-if="isModalOpen"
    :initial-form-data="formData"
    @close="() => (isModalOpen = false)"
    @create-event="handleCreateEvent"
  />
</template>

<script setup lang="ts">
import { eventService } from "@/services";
import type { CalendarEvent } from "@/services/api";
import type {
  CalendarOptions,
  DateSelectArg,
  EventApi,
  EventClickArg,
} from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import type { DateClickArg } from "@fullcalendar/interaction";
import interactionPlugin from "@fullcalendar/interaction";
import FullCalendar from "@fullcalendar/vue3";
import { usePointerSwipe } from "@vueuse/core";
import { ref, useTemplateRef } from "vue";
import CalendarModal from "./CalendarModal.vue";

const calendarOptions = ref<CalendarOptions>({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: "dayGridMonth",
  initialEvents: await eventService.getEvents().then((res) => res.items),
  editable: true,
  selectable: false, // TODO: implement selection for desktop only
  weekends: true,
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
  select: handleDateSelect,
  eventClick: handleEventClick,
  eventsSet: handleEvents,
});
const currentEvents = ref<EventApi[]>([] as EventApi[]);

const isModalOpen = ref(false);
const pointerdownTimestamp = ref(Date.now());
const formData = ref(calculateFormDataNow());
const calendarRef = useTemplateRef<InstanceType<typeof FullCalendar> & HTMLElement>(
  "fullCalendar"
);

usePointerSwipe(calendarRef, {
  onSwipeEnd(e, direction) {
    const calendarApi = calendarRef.value!.getApi();
    if (direction == "left") {
      calendarApi.next();
    } else if (direction == "right") {
      calendarApi.prev();
    }
  },
});

function handleNewEvent() {
  formData.value = calculateFormDataNow();
  isModalOpen.value = true;
}

function handleDateClick(clickInfo: DateClickArg) {
  const offset = Date.now() - pointerdownTimestamp.value;
  if (offset > 5000) {
    formData.value = calculateFormDataForDate(clickInfo.date);
    isModalOpen.value = true;
  }
}

function handleEventClick(clickInfo: EventClickArg) {
  console.log(`Clicked on ${clickInfo.event.title}`);
}

function handleEvents(events: EventApi[]) {
  currentEvents.value = events;
}

function handleDateSelect(selectInfo: DateSelectArg) {
  const calendarApi = calendarRef.value!.getApi();
  calendarApi.unselect();
  console.log(`Selected ${selectInfo.startStr} to ${selectInfo.endStr}`);
}

function handleCreateEvent(event: CalendarEvent) {
  isModalOpen.value = false;
  const calendarApi = calendarRef.value!.getApi();
  calendarApi.addEvent(event);
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
</script>

<style scoped></style>
