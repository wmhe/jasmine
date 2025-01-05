<template>
  <div class="container-fluid bg-light">
    <div class="d-flex justify-content-between fs-2">
      <div class="p-2" role="button"><i class="bi bi-list text-secondary"></i></div>
      <div class="flex-grow-1">
        <slot></slot>
      </div>
      <div class="p-2" role="button">
        <i class="bi bi-person-fill text-secondary"></i>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped></style>
