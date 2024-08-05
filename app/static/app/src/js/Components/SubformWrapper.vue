<template>
  <div :class="{ 'my-4': adding }" class="subform">
    <form
      v-bind="$attrs"
      class="subform-form"
      :class="[
        {
          'subform-ring rounded-md': adding,
        },
      ]"
    >
      <slot />
    </form>
    <slot name="viewingContainer" />
  </div>
</template>

<script setup>
defineProps({
  adding: Boolean,
});

defineOptions({
  inheritAttrs: false,
});
</script>
