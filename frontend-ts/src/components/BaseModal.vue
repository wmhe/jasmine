<template>
  <Teleport to="body">
    <div class="modal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="container">
          <div class="row g-0 m-2">
            <a class="col-4" @click="closeModal">Cancel</a>
            <div class="col-4 text-center" v-if="$slots.title">
              <slot name="title"></slot>
            </div>
            <a class="col-4 text-end" @click="doAction">Add</a>
          </div>
          <div class="row">
            <slot name="content"></slot>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
interface Emits {
  close: [];
  action: [];
}

const emit = defineEmits<Emits>();

function closeModal() {
  emit("close");
}

function doAction() {
  emit("action");
}
</script>

<style scoped>
.modal {
  position: fixed;
  display: flex;
  align-items: end;
  z-index: 2;
  height: 100%;
}
.modal-content {
  height: 90%;
}
</style>
