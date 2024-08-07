<template>
  <Link
    :href="routeUrl"
    class="inline-block rounded-t-lg border-b-2 p-4 tracking-wide"
    :class="[
      $page.url.includes(activeIfIncludes)
        ? 'border-red-600 text-red-600'
        : 'border-transparent hover:border-gray-400 hover:text-gray-700',
    ]"
  >
    {{ title }}
  </Link>
</template>
<script setup>
import { Link } from "@inertiajs/vue3";

const props = defineProps({
  title: String,
  activeIfIncludes: String,
});

const routeUrl = {
  Courses: reverseUrl("app:courses.list"),
  Topics: reverseUrl("app:topics.list"),
  "Knowledge Areas": reverseUrl("app:knowledge_areas.list"),
}[props.title];
</script>
