<template>
  <div class="flex flex-wrap justify-end gap-3 sm:mr-4 sm:flex-nowrap">
    <template v-if="adding">
      <SubformButton iconType="save" type="submit" :disabled="form.processing">
        {{ form.processing ? 'Adding...' : 'Add' }}
      </SubformButton>
      <SubformButton
        iconType="cancel"
        @click="$emit('cancelAdd')"
        :disabled="form.processing"
      >
        Cancel
      </SubformButton>
    </template>
    <SubformButton
      v-if="viewingText && !adding"
      iconType="view"
      :shouldRotateIcon="viewing"
      @click="$emit('toggleViewing')"
    >
      {{ viewing ? '' : viewingText }}
    </SubformButton>
    <template v-if="!shouldHideEditButton">
      <SubformButton
        iconType="edit"
        v-if="!editing && !adding"
        @click="$emit('edit')"
      >
        Edit
      </SubformButton>
    </template>
    <template v-if="editing">
      <SubformButton
        iconType="save"
        @click="$emit('save')"
        :disabled="form.processing"
      >
        <!-- not doing "saving..." when form is processing (like I did for the add button)
            because user might have clicked delete instead of save (both trigger form.processing) -->
        Save
      </SubformButton>
      <SubformButton
        v-if="showDeleteButton"
        iconType="delete"
        @click="$emit('delete')"
        :disabled="form.processing"
      >
        Delete
      </SubformButton>
      <SubformButton
        iconType="cancel"
        @click="$emit('cancelEditing')"
        :disabled="form.processing"
      >
        Cancel
      </SubformButton>
    </template>
  </div>
</template>

<script setup>
import SubformButton from '@/Components/SubformButton.vue';

defineProps({
  adding: Boolean,
  editing: Boolean,
  viewing: Boolean,
  viewingText: String,
  form: Object,
  showDeleteButton: {
    type: Boolean,
    default: true,
  },
  shouldHideEditButton: {
    type: Boolean,
    default: false,
  },
});

defineEmits([
  'cancelAdd',
  'save',
  'delete',
  'cancelEditing',
  'edit',
  'toggleViewing',
]);
</script>
