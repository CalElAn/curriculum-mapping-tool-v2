<template>
  <Breadcrumb class="mt-6" section="Matrix" page="Courses and Topics" />

  <div class="base-card overflow-auto p-4">
    <table
      class="w-full table-auto border-collapse border border-slate-800 text-left text-sm xl:text-base"
    >
      <thead class="thead">
        <tr>
          <th class="td p-2 text-center tracking-wide" rowspan="2">Courses</th>
          <th class="td p-2 text-center tracking-wide" :colspan="topics.length">
            Topics
          </th>
        </tr>
        <tr>
          <th
            v-for="topicHeader in topics"
            class="td p-2 text-center text-base"
          >
            {{ topicHeader.name }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" class="tbody">
          <td class="td p-2">
            <p class="font-semibold">{{ course.number }}</p>
            {{ course.title }}
          </td>
          <td
            v-for="topic in topics"
            class="td p-2 text-center font-semibold text-blue-500 hover:bg-blue-400 hover:text-white"
            v-tooltip="{
              content: getTooltipContent(course.uid, topic.uid),
              html: true,
            }"
          >
            {{ getRelationshipData(course.uid, topic.uid)?.level }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Breadcrumb from "@/Components/Breadcrumb.vue";

const props = defineProps<{
  courses: Array<object>;
  topics: Array<object>;
  coursesTeachesTopics: Array<object>;
}>();

const relationshipData = computed(() => {
  let relationshipData = {};

  props.coursesTeachesTopics.forEach((item) => {
    if (relationshipData[item.Course.uid]) {
      relationshipData[item.Course.uid][item.Topic.uid] = item.TEACHES;

      return;
    }

    relationshipData[item.Course.uid] = { [item.Topic.uid]: item.TEACHES };
  });

  return relationshipData;
});

function getRelationshipData(courseUid, topicUid) {
  return relationshipData.value[courseUid]?.[topicUid];
}

function getTooltipContent(courseUid, topicUid) {
  let tooltipData = relationshipData.value[courseUid]?.[topicUid];

  if (tooltipData)
    return `Tools: ${tooltipData.tools ?? ""}<br>Comments: ${tooltipData.comments ?? ""}`;

  return null;
}
</script>
