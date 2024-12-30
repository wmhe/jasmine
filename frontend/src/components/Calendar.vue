<template>
  <div class="container-fluid h-100 p-0">
    <div class="row h-100">
      <div class="d-flex col-sm-12 h-100">
        <FullCalendar ref="fullCalendar" :options="calendarOptions" />
      </div>
    </div>
  </div>
  <div>
    <CalendarModal
      v-if="isModalOpen"
      @close="isModalOpen = false"
      @submit="submitForm"
    ></CalendarModal>
  </div>
</template>

<script>
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import CalendarModal from "./CalendarModal.vue";
import axios from "axios";

export default {
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
            click: this.openModal,
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
    };
  },
  mounted() {
    this.$refs.fullCalendar.$el.addEventListener("touchstart", (e) => {
      this.touchstartX = e.changedTouches[0].screenX;
    });
    this.$refs.fullCalendar.$el.addEventListener("touchend", (e) => {
      this.touchendX = e.changedTouches[0].screenX;
      this.checkDirection();
    });
  },
  props: {},
  methods: {
    getEvents() {
      const path = "http://localhost:5001/api/v1/events";
      axios
        .get(path)
        .then((res) => {
          this.calendarOptions.events = res.data.events;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    checkDirection() {
      const calendarApi = this.$refs.fullCalendar.getApi();
      if (this.touchendX < this.touchstartX) {
        calendarApi.next();
      }
      if (this.touchendX > this.touchstartX) {
        calendarApi.prev();
      }
    },
    openModal() {
      this.isModalOpen = true;
    },
    handleDateClick(arg) {
      console.log("date click! " + arg.dateStr);
    },
    submitForm(data) {
      const path = "http://localhost:5001/api/v1/events";
      console.log(data);
      axios
        .post(path, data)
        .then(() => {
          this.getEvents();
          this.isModalOpen = false
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  components: {
    FullCalendar,
    CalendarModal,
  },
};
</script>
<style scoped></style>
