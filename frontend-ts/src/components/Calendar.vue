<!-- eslint-disable vue/multi-word-component-names -->
<script lang="ts">
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import FullCalendar from "@fullcalendar/vue3";
import axios from "axios";
import { defineComponent } from "vue";
import CalendarModal from "./CalendarModal.vue";

export default defineComponent({
  created() {
    this.getEvents();
  },
  data() {
    return {
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: "dayGridMonth",
        weekNumbers: true,
        customButtons: {
          menu: {
            icon: "bi bi-list fs-1 text-primary",
          },
          create: {
            icon: "bi bi-plus fs-1 text-primary",
            click: this.handleNewEvent,
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
        dateClick: this.handleDateClick,
      },
      touchstartX: 0,
      touchendX: 0,
      isModalOpen: false,
      pointerdownTimestamp: null,
      formData: null,
    };
  },
  mounted() {
    (this.$refs.fullCalendar as InstanceType<typeof FullCalendar>).$el.addEventListener(
      "touchstart",
      (e: { changedTouches: { screenX: number }[] }) => {
        this.touchstartX = e.changedTouches[0].screenX;
      }
    );
    (this.$refs.fullCalendar as InstanceType<typeof FullCalendar>).$el.addEventListener(
      "touchend",
      (e: { changedTouches: { screenX: number }[] }) => {
        this.touchendX = e.changedTouches[0].screenX;
        this.checkDirection();
      }
    );
  },
  props: {},
  methods: {
    getEvents() {
      const path = "http://localhost:5001/api/v1/events";
      axios
        .get(path)
        .then((res) => {
          // @ts-expect-error calendarOptions type undefined
          this.calendarOptions.events = res.data.items;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    checkDirection() {
      const calendarApi = (this.$refs.fullCalendar as InstanceType<
        typeof FullCalendar
      >).getApi();
      if (this.touchendX < this.touchstartX) {
        calendarApi.next();
      }
      if (this.touchendX > this.touchstartX) {
        calendarApi.prev();
      }
    },
    handleNewEvent() {
      // @ts-expect-error null problem
      this.formData = this.calculateFormDataNow();
      this.isModalOpen = true;
    },
    handleDateClick(info: { date: { getTime: () => number; }; }) {
      // @ts-expect-error null problem
      const offset = Date.now() - this.pointerdownTimestamp;
      if (offset > 1000) {
        // @ts-expect-error null problem
        this.formData = this.calculateFormDataForDate(info.date);
        this.isModalOpen = true;
      }
    },
    submitForm(data: { start: number }) {
      const path = "http://localhost:5001/api/v1/events";
      const copy = new Date(data.start);
      copy.setTime(data.start - copy.getTimezoneOffset() * 60 * 1000); // TODO: This assumes the offset is negative. Fix later.
      // @ts-expect-error need to convert to string
      data.start = copy.toISOString();
      axios
        .post(path, data)
        .then(() => {
          this.getEvents();
          this.isModalOpen = false;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    calculateFormDataNow() {
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
    },
    calculateFormDataForDate(date: { getTime: () => number }) {
      return {
        title: "",
        allDay: true,
        start: date.getTime(),
        end: date.getTime(),
      };
    },
  },
  components: {
    FullCalendar,
    CalendarModal,
  },
  computed: {
    calculateFormData() {
      if (!this.formData) {
        return this.calculateFormDataNow();
      }
      return this.formData;
    },
  },
});
</script>

<template>
  <div class="container-fluid h-100 p-0">
    <div class="row h-100">
      <div class="d-flex h-100">
        <!-- @vue-expect-error -->
        <FullCalendar ref="fullCalendar" :options="calendarOptions"></FullCalendar>
      </div>
    </div>
  </div>
  <div>
    <CalendarModal
      :initial-form-data="calculateFormData"
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @submit="submitForm"
    ></CalendarModal>
  </div>
</template>

<style scoped></style>
