<template>
  <nav class="w-full">
    <ul
      class="flex flex-wrap items-center gap-1 text-sm text-gray-700 sm:gap-2 sm:text-base sm:font-semibold"
    >
      <li class="flex items-center gap-2">
        <component :is="sectionIcon" class="h-5 w-5 text-gray-400" />
        {{ section }}
      </li>
      <li class="flex items-center">
        <svg
          aria-hidden="true"
          class="h-6 w-6 text-gray-400 sm:mr-2"
          fill="currentColor"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill-rule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clip-rule="evenodd"
          ></path>
        </svg>
        {{ page }}
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { getSectionIcon } from '@/Helpers/helpers';

const props = defineProps({
  section: String,
  page: String,
});

const sectionIcon = getSectionIcon(props.section);
</script>
