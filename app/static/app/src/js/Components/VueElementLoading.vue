<script setup lang="ts">
import VueElementLoading from 'vue-element-loading';

defineProps<{
  showLoadingSpinner: Boolean;
}>();
</script>

<template>
  <VueElementLoading
    :active="showLoadingSpinner"
    spinner="spinner"
    color="#dc2626"
  />
</template>

<style scoped></style>
