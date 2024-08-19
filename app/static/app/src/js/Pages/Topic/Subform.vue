<template>
  <SubformWrapper @submit.prevent="store()" :adding="adding" class="">
    <textarea
      :readonly="!editing && !adding"
      rows="2"
      placeholder="title"
      required
      class="input col-span-full w-full"
      type="text"
      v-model="form.title"
    ></textarea>
    <FormValidationErrors class="sm:col-span-full" :errors="form.errors" />
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
    <template v-if="viewing && uid" #viewingContainer>
      <!-- TEACHES relationship -->
      <div class="viewing-subform-container">
        <div>
          <span class="subform-title">Courses teaching this topic</span>
        </div>
        <div class="col-span-1 mt-4 flex flex-wrap gap-x-5 gap-y-3">
          <VueElementLoading :showLoadingSpinner="showTeachesLoadingSpinner" />
          <div class="w-full">
            <AddButton
              @click="addTeaches()"
              :disabled="!shouldAllowAddTeaches"
              class="my-auto text-sm"
            >
              Add a relationship
            </AddButton>
          </div>
          <TeachesSubform
            v-for="(item, index) in teachesSubformItems"
            :key="item"
            :teachesData="item"
            :topicUid="uid"
            @cancelAdd="onCancelAddTeaches()"
            @stored="shouldAllowAddTeaches = true"
            @destroyed="onDestroyedTeaches(index)"
          />
        </div>
      </div>
      <div class="viewing-subform-container mt-4">
        <div>
          <span class="subform-title"
            >Knowledge areas covered by this topic</span
          >
        </div>
        <div class="col-span-1 mt-4 flex flex-wrap gap-x-5 gap-y-3">
          <VueElementLoading :showLoadingSpinner="showCoversLoadingSpinner" />
          <div class="w-full">
            <AddButton
              @click="addCovers()"
              :disabled="!shouldAllowAddCovers"
              class="my-auto text-sm"
            >
              Add a relationship
            </AddButton>
          </div>
          <CoversSubform
            v-for="(item, index) in coversSubformItems"
            :key="item"
            :coversData="item"
            :topicUid="uid"
            @cancelAdd="onCancelAddCovers()"
            @stored="shouldAllowAddCovers = true"
            @destroyed="onDestroyedCovers(index)"
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
import TeachesSubform from '@/Pages/Topic/TeachesSubform.vue';
import CoversSubform from '@/Pages/Topic/CoversSubform.vue';
import { handleViewing, useFormHelpers } from '@/Helpers/formHelpers';
import AllSubformButtons from '@/Components/AllSubformButtons.vue';
import AddButton from '@/Components/AddButton.vue';
import VueElementLoading from '@/Components/VueElementLoading.vue';

const props = defineProps<{
  topic: Object;
}>();

const viewing = ref(false);
const showTeachesLoadingSpinner = ref(false);
const showCoversLoadingSpinner = ref(false);

const formData = {
  uid: props.topic.uid,
  title: props.topic.title,
};

const emit = defineEmits(emittedEvents);

const { uid, form, adding, editing, store, update, destroy } = useSubformHelpers(
  props.topic,
  formData,
  emit,
  reverseUrl('app:topics.store'),
  'app:topics.update',
  'app:topics.destroy',
);

// TEACHES relationship
const newTeachesRelationship = {
  TEACHES: {
    uid: null,
    level: '',
    adding: true,
  },
  Course: {
    uid: '',
  },
};

const {
  subformItems: teachesSubformItems,
  shouldAllowAdd: shouldAllowAddTeaches,
  add: addTeaches,
  onCancelAdd: onCancelAddTeaches,
  onDestroyed: onDestroyedTeaches,
} = useFormHelpers([], newTeachesRelationship);

watch(viewing, (shouldView) => {
  handleViewing(
    shouldView,
    teachesSubformItems,
    showTeachesLoadingSpinner,
    reverseUrl('app:topics.get_courses', uid.value),
  );
});

// COVERS relationship
const newCoversRelationship = {
  COVERS: {
    uid: null,
    level: '',
    adding: true,
  },
  KnowledgeArea: {
    uid: '',
  },
};

const {
  subformItems: coversSubformItems,
  shouldAllowAdd: shouldAllowAddCovers,
  add: addCovers,
  onCancelAdd: onCancelAddCovers,
  onDestroyed: onDestroyedCovers,
} = useFormHelpers([], newCoversRelationship);

watch(viewing, (shouldView) => {
  handleViewing(
    shouldView,
    coversSubformItems,
    showCoversLoadingSpinner,
    reverseUrl('app:topics.get_knowledge_areas', uid.value),
  );
});
</script>
