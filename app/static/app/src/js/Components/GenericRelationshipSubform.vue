<script setup lang="ts">
import PillDiv from '@/Components/PillDiv.vue';
import AllSubformButtons from '@/Components/AllSubformButtons.vue';
import { EllipsisVerticalIcon } from '@heroicons/vue/20/solid';
import FormValidationErrors from '@/Components/FormValidationErrors.vue';
import { computed, inject, onMounted, watch } from 'vue';
import { initFlowbite } from 'flowbite';

const props = defineProps({
  editing: Boolean,
  adding: Boolean,
  title: String,
  pillDivDisplay: String,
  form: Object,
  showTools: {
    type: Boolean,
    default: true,
  },
});

defineEmits([
  'formSubmit',
  'cancelAdd',
  'save',
  'delete',
  'cancelEditing',
  'edit',
  'toggleViewing',
]);

const level = defineModel('level');
const tools = defineModel('tools');
const comments = defineModel('comments');

const levels: Array<string> = inject('levels');

const tooltipContent = computed(() => {
  if (props.showTools) {
    return `Tools: ${tools.value}<br>Comments: ${comments.value}`;
  }

  return `Comments: ${comments.value}`;
});

const random = Math.round(Math.random() * 10000);

// Flowbite tooltip doesn't work if element was dynamically rendered after initial page initialization.
// below is necessary so the tooltip can function.
watch(
  () => props.adding,
  () => initFlowbite(),
  { flush: 'post' },
);

onMounted(() => initFlowbite());
</script>

<template>
  <form
    @submit.prevent="$emit('formSubmit')"
    class="rounded-xl border bg-white p-4 shadow shadow-sm"
    v-if="editing || adding"
    :class="{
      'subform-ring': adding,
    }"
  >
    <label class="label mt-2 block">{{ title }}</label>

    <slot />

    <label class="label mt-4 block">Level</label>
    <select required v-model="level" class="select mt-1 w-full">
      <option value="" selected disabled>- select level -</option>
      <option v-for="relationshipLevel in levels">
        {{ relationshipLevel }}
      </option>
    </select>
    <template>
      <label class="label mt-4 block">Tools</label>
      <textarea
        rows="2"
        placeholder="tools"
        class="input mt-1 w-full"
        type="text"
        v-model="tools"
      >
      </textarea>
    </template>
    <label class="label mt-4 block">Comments</label>
    <textarea
      rows="2"
      placeholder="comments"
      class="input mt-1 w-full"
      type="text"
      v-model="comments"
    ></textarea>
    <FormValidationErrors class="mt-2 sm:col-span-full" :errors="form.errors" />
    <AllSubformButtons
      class="mt-4"
      @cancelAdd="$emit('cancelAdd')"
      @save="$emit('save')"
      @delete="$emit('delete')"
      @cancelEditing="$emit('cancelEditing')"
      @edit="$emit('edit')"
      @toggleViewing="$emit('toggleViewing')"
      :adding="adding"
      :editing="editing"
      :form="form"
    />
  </form>
  <PillDiv
    v-tooltip="{
      content: tooltipContent,
      html: true,
    }"
    class="my-auto"
    v-else
  >
    {{ pillDivDisplay }}

    <button
      id="dropdownMenuIconButton"
      :data-dropdown-toggle="`dropdownDots${random}`"
      data-dropdown-placement="right"
      class="inline-flex items-center p-1 text-gray-900"
      type="button"
    >
      <EllipsisVerticalIcon class="h-5 w-5" />
    </button>

    <!-- Dropdown menu -->
    <div
      :id="`dropdownDots${random}`"
      class="z-10 hidden w-44 space-y-2 divide-y divide-gray-100 rounded-2xl bg-white py-2 text-sm shadow dark:divide-gray-600 dark:bg-gray-700"
    >
      <ul
        class="px-2 text-gray-700 dark:text-gray-200"
        aria-labelledby="dropdownMenuIconButton"
      >
        <li>
          <button
            @click="$emit('edit')"
            class="block w-full px-2 py-1 text-start hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
          >
            Edit
          </button>
        </li>
      </ul>
      <!--      <div class="px-2">
        <a
          href="#"
          class="block px-2 py-1 text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
          >Link to Course Outcome</a
        >
      </div>-->
    </div>
  </PillDiv>
</template>

<style scoped></style>
