<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <FullCalendar ref="fullCalendar" :options="calendarOptions" />
</template>

<script setup lang="ts">
import type { CalendarEvent } from "@/services/api";
import type {
  CalendarOptions,
  DateSelectArg,
  DatesSetArg,
  EventApi,
  EventClickArg,
} from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import type { DateClickArg } from "@fullcalendar/interaction";
import interactionPlugin from "@fullcalendar/interaction";
import FullCalendar from "@fullcalendar/vue3";
import { usePointerSwipe } from "@vueuse/core";
import { ref, useTemplateRef, watchEffect } from "vue";

interface Props {
  events: CalendarEvent[];
}
interface Emits {
  change: [title: string];
  openCreateEventModalAtDate: [date: Date];
}
const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const calendarOptions = ref<CalendarOptions>({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: "dayGridMonth",
  editable: false, // TODO: implement dragabble events for desktop only
  selectable: false, // TODO: implement selection for desktop only
  weekends: true,
  weekNumbers: true,
  headerToolbar: false,
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
  datesSet: handleDates,
});
const pointerdownTimestamp = ref(Date.now());
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

function handleDateClick(clickInfo: DateClickArg) {
  const offset = Date.now() - pointerdownTimestamp.value;
  if (offset > 5000) {
    emit("openCreateEventModalAtDate", clickInfo.date);
  }
}

function handleEventClick(clickInfo: EventClickArg) {
  console.log(`Clicked on ${clickInfo.event.title}`);
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function handleEvents(events: EventApi[]) {
  console.log("Events updated");
}

function handleDateSelect(selectInfo: DateSelectArg) {
  const calendarApi = calendarRef.value!.getApi();
  calendarApi.unselect();
  console.log(`Selected ${selectInfo.startStr} to ${selectInfo.endStr}`);
}

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function handleDates(datesSet: DatesSetArg) {
  const calendarApi = calendarRef.value!.getApi();
  emit("change", calendarApi.getCurrentData().viewTitle);
}

watchEffect(() => {
  calendarOptions.value.events = props.events;
});
</script>

<style scoped></style>
