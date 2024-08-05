<template>
  <button
    :type="type"
    :class="[buttonColours]"
    class="my-auto flex flex-wrap items-center justify-between gap-1 rounded-lg border px-2 py-1 text-sm font-medium tracking-wide shadow-sm hover:border-transparent hover:text-white disabled:opacity-50 disabled:hover:cursor-text xl:font-semibold xl:tracking-wider"
  >
    <component
      :is="icon"
      class="h-5 w-5 transition-transform"
      :class="{ 'rotate-180': shouldRotateIcon }"
    />
    <slot />
  </button>
</template>

<script setup>
import {
  ArrowDownCircleIcon,
  CheckIcon,
  PencilSquareIcon,
  TrashIcon,
  XMarkIcon,
} from '@heroicons/vue/24/outline';
import { computed } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'button',
  },
  iconType: String,
  shouldRotateIcon: { type: Boolean, default: false },
});

const icon = {
  view: ArrowDownCircleIcon,
  edit: PencilSquareIcon,
  save: CheckIcon,
  delete: TrashIcon,
  cancel: XMarkIcon,
}[props.iconType];

const buttonColours = computed(() => {
  if (props.iconType === 'delete')
    return 'border-red-600 text-red-600 hover:bg-red-400';

  if (props.iconType === 'view')
    return 'border-blue-600 text-blue-600 hover:bg-blue-400';

  return 'border-amber-600 text-amber-600 hover:bg-amber-400';
});
</script>
