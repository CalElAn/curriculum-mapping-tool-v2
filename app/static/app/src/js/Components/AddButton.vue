<template>
  <button
    :type="type"
    class="inline-flex flex-wrap items-center justify-center gap-1 rounded-lg border border-red-600 px-2 py-1 tracking-wide text-red-600 shadow-sm hover:bg-red-100 disabled:opacity-50"
  >
    <PlusCircleIcon class="h-5 w-5" />
    <slot />
  </button>
</template>

<script setup>
import { PlusCircleIcon } from '@heroicons/vue/24/outline';

defineProps({
  type: {
    type: String,
    default: 'button',
  },
});
</script>
