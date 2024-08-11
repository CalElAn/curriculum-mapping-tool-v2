<template>
  <Breadcrumb class="mt-6" section="Matrix" page="Topics and Knowledge Areas" />

  <div class="base-card overflow-auto p-4">
    <table
      class="w-full table-auto border-collapse border border-slate-800 text-left text-sm xl:text-base"
    >
      <thead class="thead">
        <tr>
          <th class="td p-2 text-center tracking-wide" rowspan="2">Topics</th>
          <th
            class="td p-2 text-center tracking-wide"
            :colspan="knowledgeAreas.length"
          >
            Knowledge Areas
          </th>
        </tr>
        <tr>
          <th
            v-for="knowledgeAreaHeader in knowledgeAreas"
            class="td p-2 text-center text-base font-normal"
          >
            {{ knowledgeAreaHeader.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="topic in topics" class="tbody">
          <td class="td p-2">
            {{ topic.name }}
          </td>
          <td
            v-for="knowledgeArea in knowledgeAreas"
            class="td p-2 text-center font-semibold text-blue-500 hover:bg-blue-400 hover:text-white"
            v-tooltip="{
              content: getTooltipContent(topic.uid, knowledgeArea.uid),
              html: true,
            }"
          >
            {{ getRelationshipData(topic.uid, knowledgeArea.uid)?.level }}
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
  topics: Array<object>;
  knowledgeAreas: Array<object>;
  topicsCoversKnowledgeAreas: Array<object>;
}>();

const relationshipData = computed(() => {
  let relationshipData = {};

  props.topicsCoversKnowledgeAreas.forEach((item) => {
    if (relationshipData[item.Topic.uid]) {
      relationshipData[item.Topic.uid][item.KnowledgeArea.uid] = item.COVERS;

      return;
    }

    relationshipData[item.Topic.uid] = {
      [item.KnowledgeArea.uid]: item.COVERS,
    };
  });

  return relationshipData;
});

function getRelationshipData(topicUid, knowledgeAreaUid) {
  return relationshipData.value[topicUid]?.[knowledgeAreaUid];
}

function getTooltipContent(topicUid, knowledgeAreaUid) {
  let tooltipData = relationshipData.value[topicUid]?.[knowledgeAreaUid];

  if (tooltipData)
    return `Tools: ${tooltipData.tools ?? ""}<br>Comments: ${tooltipData.comments ?? ""}`;

  return null;
}
</script>
