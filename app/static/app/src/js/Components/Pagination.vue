<template>
  <div class="flex flex-wrap justify-center gap-2">
    <component
      v-if="pageObj.hasPrevious"
      :is="shouldPaginateWithAxios ? 'button' : Link"
      @click="
        shouldPaginateWithAxios
          ? visitLink(`?page=${pageObj.previousPageNumber}`)
          : ''
      "
      :href="`?page=${pageObj.previousPageNumber}`"
      class="mb-1 rounded-lg border px-4 py-3 leading-4 shadow-sm hover:border-red-600 hover:text-red-600 focus:border-red-600 focus:text-red-600"
    >
      &laquo; previous
    </component>
    <template v-if="pageObj.numPages > 1">
      <template
        v-for="pageNumber in pageObj.pageRange"
        :key="`link-${pageNumber}`"
      >
        <component
          :is="shouldPaginateWithAxios ? 'button' : Link"
          @click="
            shouldPaginateWithAxios ? visitLink(`?page=${pageNumber}`) : ''
          "
          :href="`?page=${pageNumber}`"
          class="mb-1 rounded-lg border px-4 py-3 leading-4 shadow-sm hover:border-red-600 hover:text-red-600 focus:border-red-600 focus:text-red-600"
          :class="[
            pageObj.currentPage === pageNumber
              ? 'border-red-600 font-semibold text-red-600'
              : 'border-gray-400 text-gray-500',
          ]"
          >{{ pageNumber }}
        </component>
      </template>
    </template>
    <component
      v-if="pageObj.hasNext"
      :is="shouldPaginateWithAxios ? 'button' : Link"
      @click="
        shouldPaginateWithAxios
          ? visitLink(`?page=${pageObj.nextPageNumber}`)
          : ''
      "
      :href="`?page=${pageObj.nextPageNumber}`"
      class="mb-1 rounded-lg border px-4 py-3 leading-4 shadow-sm hover:border-red-600 hover:text-red-600 focus:border-red-600 focus:text-red-600"
    >
      next &raquo;
    </component>
  </div>
</template>

<script setup>
import { Link } from "@inertiajs/vue3";

const props = defineProps({
  pageObj: Object,
  shouldPaginateWithAxios: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["visitedLink"]);

function visitLink(url) {
  axios.get(url).then((response) => {
    emit("visitedLink", response.data);
  });
}
</script>
