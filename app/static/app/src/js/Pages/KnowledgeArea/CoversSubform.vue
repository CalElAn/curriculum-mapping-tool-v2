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
    v-model:tools="form.tools"
    v-model:level="form.level"
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
  coversData: Object;
  knowledgeAreaUid: String;
}>();

const allTopics: Array<string> = inject("allTopics");

const emit = defineEmits(emittedEvents);

const useFormData = {
  uid: props.coversData.COVERS.uid,
  level: props.coversData.COVERS.level ?? "",
  tools: props.coversData.COVERS.tools ?? "",
  comments: props.coversData.COVERS.comments ?? "",
  topic_uid: props.coversData.Topic.uid,
  knowledge_area_uid: props.knowledgeAreaUid,
};

const { form, adding, editing, store, update, destroy, uid } =
  useSubformHelpers(
    props.coversData.COVERS,
    useFormData,
    emit,
    reverseUrl("app:covers.store"),
    "app:covers.update",
    "app:covers.destroy",
  );

const topicTitle = computed(
  () => allTopics.find((topic) => topic.uid === form.topic_uid)?.title,
);
</script>
