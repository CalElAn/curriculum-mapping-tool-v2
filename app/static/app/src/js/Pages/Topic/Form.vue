<template>
  <Head title="Data Entry | Topics" />

  <Breadcrumb class="mt-6" section="Data Entry" page="Topics" />

  <div class="form-card">
    <p class="form-title mt-2 text-center">Topics</p>
    <div class="mt-6">
      <div
        class="mb-2 mt-8 flex flex-col items-center justify-between gap-y-3 md:mt-8 lg:flex-row"
      >
        <div
          class="flex w-full justify-center gap-1 sm:flex-row sm:items-center lg:w-3/5 xl:gap-4 xl:text-base"
        >
          <MagnifyingGlassIcon class="hidden h-5 w-5 text-gray-500 sm:block" />
          <input
            v-model="filter"
            class="input w-full shadow-sm sm:grow"
            placeholder="Search..."
            type="text"
          />
        </div>
        <AddButton
          @click="add()"
          :disabled="!shouldAllowAdd"
          class="w-full font-semibold sm:mr-4 sm:w-fit"
        >
          Add a topic
        </AddButton>
      </div>
      <div class="mt-3 flex flex-col text-sm md:text-base">
        <TransitionGroup name="list">
          <Subform
            v-for="(topic, index) in subformItems"
            :key="topic"
            :topic="topic"
            @cancelAdd="onCancelAdd()"
            @stored="shouldAllowAdd = true"
            @destroyed="onDestroyed(index)"
          />
        </TransitionGroup>

        <p v-if="!subformItems || subformItems.length === 0" class="ml-2">
          No topics found
        </p>
      </div>
      <Pagination class="mt-6 flex w-11/12 justify-start" :pageObj="pageObj" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { MagnifyingGlassIcon } from "@heroicons/vue/24/solid";
import { Head } from "@inertiajs/vue3";
import AddButton from "@/Components/AddButton.vue";
import Subform from "@/Pages/Topic/Subform.vue";
import { useFormHelpers } from "@/Helpers/formHelpers";
import { provide, ref, watch } from "vue";
import Pagination from "@/Components/Pagination.vue";
import throttle from "lodash/throttle";
import { getFilteredItems } from "@/Helpers/helpers";
import Breadcrumb from "@/Components/Breadcrumb.vue";

const props = defineProps<{
  initialTopics: Object;
  pageObj: Object;
  allCourses: Array<object>;
  allKnowledgeAreas: Array<object>;
  levels: Array<string>;
  filter: string | null;
}>();

provide("allCourses", props.allCourses);
provide("allKnowledgeAreas", props.allKnowledgeAreas);
provide("levels", props.levels);

const filter = ref(props.filter);

const newTopic = {
  uid: null,
  title: null,
};

const { subformItems, shouldAllowAdd, add, onCancelAdd, onDestroyed } =
  useFormHelpers(props.initialTopics, newTopic);

watch(
  filter,
  throttle(
    () =>
      getFilteredItems(
        reverseUrl("app:topics.list"),
        filter.value,
        subformItems,
        "initialTopics",
      ),
    150,
  ),
);
</script>

<style scoped>
@import "../../../css/subform_transition.css";
</style>
