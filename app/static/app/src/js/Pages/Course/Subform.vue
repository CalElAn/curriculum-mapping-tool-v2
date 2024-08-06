<template>
  <SubformWrapper @submit.prevent="store()" :adding="adding" class="">
    <input
      :readonly="!editing && !adding"
      type="number"
      step="any"
      placeholder="number"
      class="input col-span-full w-full"
      v-model="form.number"
    />
    <textarea
      :readonly="!editing && !adding"
      rows="2"
      placeholder="name"
      required
      class="input col-span-full w-full"
      type="text"
      v-model="form.title"
    ></textarea>
    <FormValidationErrors class="sm:col-span-full" :errors="form.errors" />
    <div class="flex justify-end sm:col-span-full sm:mr-4">
      <AllSubformButtons
        class=""
        @cancelAdd="$emit('cancelAdd')"
        @save="update()"
        @delete="destroy()"
        @cancelEditing="editing = false"
        @edit="editing = true"
        @toggleViewing="viewing = !viewing"
        :adding="adding"
        :editing="editing"
        :viewing="viewing"
        :viewingText="`Relationships`"
        :form="form"
      />
    </div>
    <template v-if="viewing && uid" #viewingContainer>
      <div class="viewing-subform-container">
        <div>
          <span class="subform-title">Topics taught by this course</span>
        </div>
        <div class="col-span-1 mt-4 flex flex-wrap gap-x-5 gap-y-3">
          <VueElementLoading :showLoadingSpinner="showLoadingSpinner" />
          <AddButton
            @click="add()"
            :disabled="!shouldAllowAdd"
            class="my-auto text-sm"
          >
            Add a relationship
          </AddButton>
          <TeachesSubform
            v-for="(item, index) in subformItems"
            :key="item"
            :teachesData="item"
            :courseUid="uid"
            @cancelAdd="onCancelAdd()"
            @stored="shouldAllowAdd = true"
            @destroyed="onDestroyed(index)"
          />
        </div>
      </div>
    </template>
  </SubformWrapper>
</template>

<script setup lang="ts">
import SubformWrapper from "@/Components/SubformWrapper.vue";
import FormValidationErrors from "@/Components/FormValidationErrors.vue";
import { emittedEvents, useSubformHelpers } from "@/Helpers/subformHelpers.js";
import { ref, watch } from "vue";
import TeachesSubform from "@/Pages/Course/TeachesSubform.vue";
import { handleViewing, useFormHelpers } from "@/Helpers/formHelpers";
import AddButton from "@/Components/AddButton.vue";
import SubformButton from "@/Components/SubformButton.vue";
import VueElementLoading from "@/Components/VueElementLoading.vue";
import AllSubformButtons from "@/Components/AllSubformButtons.vue";

const props = defineProps<{
  course: Object;
}>();

const viewing = ref(false);
const showLoadingSpinner = ref(false);

const useFormData = {
  uid: props.course.uid,
  number: props.course.number,
  title: props.course.title,
};

const emit = defineEmits(emittedEvents);

const { uid, form, adding, editing, store, update, destroy } = useSubformHelpers(
  props.course,
  useFormData,
  emit,
  window.reverseUrl("app:courses.store"),
  "app:courses.update",
  "app:courses.destroy",
);

const newTeachesRelationship = {
  TEACHES: {
    uid: null,
    level: "",
    adding: true,
  },
  Topic: {
    uid: "",
  },
};

const { subformItems, shouldAllowAdd, add, onCancelAdd, onDestroyed } =
  useFormHelpers([], newTeachesRelationship);

watch(viewing, (shouldView) => {
  handleViewing(
    shouldView,
    subformItems,
    showLoadingSpinner,
    window.reverseUrl("app:courses.get_topics", uid.value),
  );
});
</script>
