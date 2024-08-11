<template>
  <li
    :class="[
      isDropdownActive()
        ? 'bg-red-200 font-semibold text-red-600'
        : 'font-medium hover:text-red-600',
    ]"
    class="rounded-lg"
  >
    <button
      @click="shouldOpenDropdown = !shouldOpenDropdown"
      class="flex w-full items-center justify-start gap-2 py-2 pl-3 tracking-wide"
    >
      <component :is="icon" class="h-5 w-5 shrink-0 text-red-700" />
      <span class="shrink-0">{{ section }}</span>
      <ChevronDownIconSolid
        class="ml-auto mr-2 h-6 w-6 shrink-0 justify-self-end text-red-700 transition-transform"
        :class="{ 'rotate-180': shouldOpenDropdown }"
      />
    </button>
    <ul
      v-show="shouldOpenDropdown"
      class="ml-5 space-y-3 px-2 pb-3 pt-1 text-sm font-normal text-red-900"
    >
      <li v-for="dropdownItem in dropdownItems">
        <Link
          :href="dropdownItem.href"
          :class="[
            isDropdownItemActive(dropdownItem.activeUrls)
              ? '-m-2 my-2 mb-1 border-l-2 border-gray-800 p-1.5 font-semibold tracking-wide text-gray-800'
              : 'hover:text-red-600',
          ]"
          class="flex items-center hover:underline"
          >{{ dropdownItem.label }}
        </Link>
      </li>
    </ul>
  </li>
</template>

<script setup>
import { computed, ref } from "vue";
import { usePage, Link } from "@inertiajs/vue3";
import { ChevronDownIcon as ChevronDownIconSolid } from "@heroicons/vue/20/solid";
import { getSectionIcon } from "@/Helpers/helpers";

const props = defineProps({
  section: String,
  initialShouldOpenDropdown: Boolean,
  activeDropdownUrls: Array,
  dropdownItems: Array,
});

const icon = getSectionIcon(props.section);

const shouldOpenDropdown = ref(false);

const emit = defineEmits(["openDropdown"]);

function isDropdownActive() {
  let isDropdownActive = false;

  for (const dropdownUrl of props.activeDropdownUrls) {
    if (usePage().url.includes(dropdownUrl)) {
      isDropdownActive = true;
      break;
    }
  }

  return isDropdownActive;
}

function isDropdownItemActive(activeUrls) {
  let isDropdownItemActive = false;

  activeUrls.forEach((activeUrl) => {
    if (usePage().url.includes(activeUrl) && isDropdownActive()) {
      isDropdownItemActive = true;
    }
  });

  return isDropdownItemActive;
}
</script>
