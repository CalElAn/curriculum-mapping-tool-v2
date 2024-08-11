<template>
  <Head title="Data Entry | Knowledge Areas" />

  <Breadcrumb class="mt-6" section="Data Entry" page="Knowledge Areas"/>

  <div class="form-card">
    <p class="form-title mt-2 text-center">Knowledge Areas</p>
    <div class="mt-6">
      <div
        class="mb-2 mt-8 flex flex-col items-center justify-between gap-y-3 md:mt-8 lg:flex-row"
      >
        <div
          class="flex w-full flex-row items-center justify-center gap-1 lg:w-3/5 xl:gap-4 xl:text-base"
        >
          <MagnifyingGlassIcon
            class="h-4 w-4 text-gray-500 sm:block sm:h-5 sm:w-5"
          />
          <input
            v-model="filter"
            class="input w-full shadow-sm"
            placeholder="Search..."
            type="text"
          />
        </div>
        <AddButton
          @click="add()"
          :disabled="!shouldAllowAdd"
          class="mr-4 font-semibold"
        >
          Add a knowledge area
        </AddButton>
      </div>
      <div class="mt-3 flex flex-col text-sm md:text-base">
        <TransitionGroup name="list">
          <Subform
            v-for="(knowledgeArea, index) in subformItems"
            :key="knowledgeArea"
            :knowledgeArea="knowledgeArea"
            @cancelAdd="onCancelAdd()"
            @stored="shouldAllowAdd = true"
            @destroyed="onDestroyed(index)"
          />
        </TransitionGroup>

        <p v-if="!subformItems || subformItems.length === 0" class="ml-2">
          No Knowledge Areas found
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
import Subform from "@/Pages/KnowledgeArea/Subform.vue";
import { useFormHelpers } from "@/Helpers/formHelpers";
import { provide, ref, watch } from "vue";
import Pagination from "@/Components/Pagination.vue";
import throttle from "lodash/throttle";
import { getFilteredItems } from "@/Helpers/helpers";
import Breadcrumb from "@/Components/Breadcrumb.vue";

const props = defineProps<{
  initialKnowledgeAreas: Object;
  pageObj: Object;
  allTopics: Array<object>;
  levels: Array<string>;
  filter: string | null;
}>();

provide("allTopics", props.allTopics);
provide("levels", props.levels);

const filter = ref(props.filter);

const newCourse = {
  uid: null,
  number: null,
  title: null,
};

const { subformItems, shouldAllowAdd, add, onCancelAdd, onDestroyed } =
  useFormHelpers(props.initialKnowledgeAreas, newCourse);

watch(
  filter,
  throttle(
    () =>
      getFilteredItems(
        reverseUrl("app:knowledge_areas.form"),
        filter.value,
        subformItems,
        "initialKnowledgeAreas",
      ),
    150,
  ),
);
</script>

<style scoped>
@import "../../../css/subform_transition.css";
</style>
