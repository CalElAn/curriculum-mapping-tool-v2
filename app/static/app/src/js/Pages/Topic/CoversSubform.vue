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
    :pillDivDisplay="`${knowledgeAreaTitle} | ${form.level}`"
    :showTools="false"
    v-model:level="form.level"
    v-model:comments="form.comments"
  >
    <select
      :disabled="editing"
      required
      v-model="form.knowledge_area_uid"
      class="select mt-1 w-full"
    >
      <option value="" selected disabled>- select knowledge area -</option>
      <option
        v-for="knowledgeArea in allKnowledgeAreas"
        :value="knowledgeArea.uid"
      >
        {{ knowledgeArea.title }}
      </option>
    </select>
  </GenericRelationshipSubform>
</template>

<script setup lang="ts">
import GenericRelationshipSubform from '@/Components/GenericRelationshipSubform.vue';
import { emittedEvents, useSubformHelpers } from '@/Helpers/subformHelpers.js';
import { onMounted, watch, computed, inject } from 'vue';

const props = defineProps<{
  coversData: Object;
  topicUid: String;
}>();

const allKnowledgeAreas: Array<string> = inject('allKnowledgeAreas');

const emit = defineEmits(emittedEvents);

const useFormData = {
  uid: props.coversData.COVERS.uid,
  level: props.coversData.COVERS.level ?? '',
  tools: props.coversData.COVERS.tools ?? '',
  comments: props.coversData.COVERS.comments ?? '',
  topic_uid: props.topicUid,
  knowledge_area_uid: props.coversData.KnowledgeArea.uid,
};

const { form, adding, editing, store, update, destroy, uid } = useSubformHelpers(
  props.coversData.COVERS,
  useFormData,
  emit,
  reverseUrl('app:covers.store'),
  'app:covers.update',
  'app:covers.destroy',
);

const knowledgeAreaTitle = computed(
  () =>
    allKnowledgeAreas.find(
      (knowledgeArea) => knowledgeArea.uid === form.knowledge_area_uid,
    )?.title,
);
</script>
