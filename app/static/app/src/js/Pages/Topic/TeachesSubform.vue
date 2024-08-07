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
    title="Course"
    :pillDivDisplay="`${courseNumber} | ${form.level}`"
    v-model:level="form.level"
    v-model:tools="form.tools"
    v-model:comments="form.comments"
  >
    <select
      :disabled="editing"
      required
      v-model="form.course_uid"
      class="select mt-1 w-full"
    >
      <option value="" selected disabled>- select course -</option>
      <option v-for="course in allCourses" :value="course.uid">
        {{ course.number }}
      </option>
    </select>
  </GenericRelationshipSubform>
</template>

<script setup lang="ts">
import { emittedEvents, useSubformHelpers } from '@/Helpers/subformHelpers.js';
import { onMounted, watch, computed, inject } from 'vue';
import GenericRelationshipSubform from '@/Components/GenericRelationshipSubform.vue';

const props = defineProps<{
  teachesData: Object;
  topicUid: String;
}>();

const allCourses: Array<string> = inject('allCourses');

const emit = defineEmits(emittedEvents);

const useFormData = {
  uid: props.teachesData.TEACHES.uid,
  level: props.teachesData.TEACHES.level ?? '',
  tools: props.teachesData.TEACHES.tools ?? '',
  comments: props.teachesData.TEACHES.comments ?? '',
  course_uid: props.teachesData.Course.uid,
  topic_uid: props.topicUid,
};

const { form, adding, editing, store, update, destroy, uid } = useSubformHelpers(
  props.teachesData.TEACHES,
  useFormData,
  emit,
  reverseUrl('app:teaches.store'),
  'app:teaches.update',
  'app:teaches.destroy',
);

const courseNumber = computed(
  () => allCourses.find((course) => course.uid === form.course_uid)?.number,
);
</script>
