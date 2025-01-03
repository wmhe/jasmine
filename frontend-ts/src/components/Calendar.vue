<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="container-fluid h-100 p-0">
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
import axios from "axios";
import { onMounted, ref, useTemplateRef } from "vue";
import CalendarModal from "./CalendarModal.vue";
import type { Event } from "@/services/api";

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
  events: [],
});

const touchstartX = ref(0);
const touchendX = ref(0);
const isModalOpen = ref(false);
const pointerdownTimestamp = ref(Date.now());
const formData = ref(calculateFormDataNow());
const calendarRef = useTemplateRef<FullCalendarType>("fullCalendar");

function getEvents() {
  const path = "http://localhost:5001/api/v1/events";
  axios
    .get(path)
    .then((res) => {
      calendarOptions.value.events = res.data.items;
    })
    .catch((error) => {
      console.error(error);
    });
}

onMounted(() => {
  getEvents();
  calendarRef.value?.$el.addEventListener(
    "touchstart",
    (e: { changedTouches: { screenX: number }[] }) => {
      touchstartX.value = e.changedTouches[0].screenX;
    }
  );
  calendarRef.value?.$el.addEventListener(
    "touchend",
    (e: { changedTouches: { screenX: number }[] }) => {
      touchendX.value = e.changedTouches[0].screenX;
      checkDirection();
    }
  );
});

function checkDirection() {
  if (touchendX.value < touchstartX.value) {
    calendarRef.value?.getApi().next();
  }
  if (touchendX.value > touchstartX.value) {
    calendarRef.value?.getApi().prev();
  }
}

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

function submitForm(data: Event) {
  const path = "http://localhost:5001/api/v1/events";
  const copy = new Date(data.start);
  copy.setTime(data.start - copy.getTimezoneOffset() * 60 * 1000); // TODO: This assumes the offset is negative. Fix later.
  // @ts-expect-error type cast to string
  data.start = copy.toISOString();
  axios
    .post(path, data)
    .then(() => {
      getEvents();
      isModalOpen.value = false;
    })
    .catch((error) => {
      console.error(error);
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
</script>

<style scoped></style>
