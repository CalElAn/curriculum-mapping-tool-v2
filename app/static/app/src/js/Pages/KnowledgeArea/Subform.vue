<template>
  <SubformWrapper @submit.prevent="store()" :adding="adding" class="">
    <input
      :readonly="!editing && !adding"
      placeholder="title"
      type="text"
      class="input col-span-full w-full"
      v-model="form.title"
    />
    <textarea
      :readonly="!editing && !adding"
      rows="2"
      placeholder="description"
      required
      class="input col-span-full w-full"
      type="text"
      v-model="form.description"
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
          <span class="subform-title"
            >Topics that cover this knowledge area</span
          >
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
          <CoversSubform
            v-for="(item, index) in subformItems"
            :key="item"
            :coversData="item"
            :knowledgeAreaUid="uid"
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
import SubformWrapper from '@/Components/SubformWrapper.vue';
import FormValidationErrors from '@/Components/FormValidationErrors.vue';
import { emittedEvents, useSubformHelpers } from '@/Helpers/subformHelpers.js';
import { ref, watch } from 'vue';
import CoversSubform from '@/Pages/KnowledgeArea/CoversSubform.vue';
import { handleViewing, useFormHelpers } from '@/Helpers/formHelpers';
import AddButton from '@/Components/AddButton.vue';
import SubformButton from '@/Components/SubformButton.vue';
import VueElementLoading from '@/Components/VueElementLoading.vue';
import AllSubformButtons from '@/Components/AllSubformButtons.vue';

const props = defineProps<{
  knowledgeArea: Object;
}>();

const viewing = ref(false);
const showLoadingSpinner = ref(false);

const formData = {
  uid: props.knowledgeArea.uid,
  title: props.knowledgeArea.title,
  description: props.knowledgeArea.description,
};

const emit = defineEmits(emittedEvents);

const { uid, form, adding, editing, store, update, destroy } = useSubformHelpers(
  props.knowledgeArea,
  formData,
  emit,
  reverseUrl('app:knowledge_areas.store'),
  'app:knowledge_areas.update',
  'app:knowledge_areas.destroy',
);

const newTeachesRelationship = {
  COVERS: {
    uid: null,
    level: '',
    adding: true,
  },
  Topic: {
    uid: '',
  },
};

const { subformItems, shouldAllowAdd, add, onCancelAdd, onDestroyed } =
  useFormHelpers([], newTeachesRelationship);

watch(viewing, (shouldView) => {
  handleViewing(
    shouldView,
    subformItems,
    showLoadingSpinner,
    reverseUrl('app:knowledge_areas.get_topics', uid.value),
  );
});
</script>
