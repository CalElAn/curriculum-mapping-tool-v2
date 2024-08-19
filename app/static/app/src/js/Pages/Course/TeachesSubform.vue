<template>
  <GenericRelationshipSubform
    @formSubmit="store()"
    @save="update()"
    @delete="destroy()"
    @cancelAdd="$emit('cancelAdd')"
    @cancelEditing="editing = false"
    @edit="editing = true"
    @toggleViewing="viewing = !viewing"
    :editing="editing"
    :adding="adding"
    :form="form"
    title="Topic"
    :pillDivDisplay="`${topicTitle} | ${form.level}`"
    v-model:level="form.level"
    v-model:tools="form.tools"
    v-model:comments="form.comments"
  >
    <select
      :disabled="editing"
      required
      v-model="form.topic_uid"
      class="select mt-1 w-full"
    >
      <option value="" selected disabled>- select topic -</option>
      <option v-for="topic in allTopics" :value="topic.uid">
        {{ topic.title }}
      </option>
    </select>
  </GenericRelationshipSubform>
</template>

<script setup lang="ts">
import GenericRelationshipSubform from "@/Components/GenericRelationshipSubform.vue";
import { emittedEvents, useSubformHelpers } from "@/Helpers/subformHelpers.js";
import { onMounted, watch, computed, inject } from "vue";

const props = defineProps<{
  teachesData: Object;
  courseUid: String;
}>();

const allTopics: Array<string> = inject("allTopics");

const emit = defineEmits(emittedEvents);

const useFormData = {
  uid: props.teachesData.TEACHES.uid,
  level: props.teachesData.TEACHES.level ?? "",
  tools: props.teachesData.TEACHES.tools ?? "",
  comments: props.teachesData.TEACHES.comments ?? "",
  topic_uid: props.teachesData.Topic.uid,
  course_uid: props.courseUid
};

const { form, adding, editing, store, update, destroy, uid } = useSubformHelpers(
  props.teachesData.TEACHES,
  useFormData,
  emit,
  reverseUrl("app:teaches.store"),
  "app:teaches.update",
  "app:teaches.destroy"
);

const topicTitle = computed(
  () => allTopics.find((topic) => topic.uid === form.topic_uid)?.title
);
</script>
