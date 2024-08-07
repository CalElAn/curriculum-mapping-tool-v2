<script setup lang="ts">
import { Head } from '@inertiajs/vue3';
import { onMounted, ref, watch } from 'vue';
import { DataSet, Network } from 'vis-network/standalone';
import PillDiv from '@/Components/PillDiv.vue';
import map from 'lodash/map';

const props = defineProps<{
  courses: Array<object>;
  topics: Array<object>;
  knowledgeAreas: Array<object>;
  coursesWithTopics: Array<object>;
  prerequisiteCourses: Array<object>;
  knowledgeAreasWithTopics: Array<object>;
  levels: Array<string>;
}>();

const courseNumbers = map(props.courses, 'number');
const prereqData = props.prerequisiteCourses.filter(
  (item) =>
    courseNumbers.includes(item.Course_from.number) &&
    courseNumbers.includes(item.Course_to.number),
);

const relationships = {
  Prerequisites: map(prereqData, 'IS_PREREQUISITE_OF'),
  Teaches: map(props.coursesWithTopics, 'TEACHES'),
  Covers: map(props.knowledgeAreasWithTopics, 'COVERS'),
};
const selectedRelationships = ref(Object.keys(relationships));

const allCourses: Array<Number> = props.courses.map((course) => course.number);
const selectedCourses = ref(allCourses);
const selectAll = ref(true);

watch(selectedCourses, (newSelectedCourses) => {
  if (newSelectedCourses.length === 0) selectAll.value = false;

  if (newSelectedCourses.length === props.courses.length)
    selectAll.value = true;
});

watch(selectAll, (newVal) => {
  if (newVal) {
    /* This second check is to prevent the "toggleCourseVisibility" function from being called twice.
       Without the check, the function is called once when the last item is added to selectedCourses,
       and again when the watcher on selectedCourses sets the value of selectAll to true*/
    if (selectedCourses.value.length < props.courses.length) {
      selectedCourses.value.push(
        ...props.courses.map((course) => course.number),
      );

      props.courses.forEach((course) => {
        toggleCourseVisibility(course.uid, true);
      });
    }

    return;
  }

  /* This check is also to prevent the "toggleCourseVisibility" function from being called twice.
     Without the check, the function is called once when the last item is removed from selectedCourses,
     and again when the watcher on selectedCourses sets the value of selectAll to false*/
  if (selectedCourses.value.length > 0) {
    selectedCourses.value = [];

    props.courses.forEach((course) => {
      toggleCourseVisibility(course.uid, false);
    });
  }
});

let nodes = [];

nodes.push(
  ...props.courses.map((course) => ({
    id: course.uid,
    label: `<b>${course.number}</b>`,
    title: `Course
      Number: ${course.number}
      Title: ${course.title}`,
    color: '#fca5a5',
    mass: 4,
    font: { multi: true, bold: 20, size: 20 },
    widthConstraint: { minimum: 70 },
    heightConstraint: { minimum: 70 },
  })),
);

nodes.push(
  ...props.topics.map((topic) => ({
    id: topic.uid,
    label: truncateText(topic.name),
    title: `Topic\nName: ${topic.name}`,
    font: { size: 16 },
    widthConstraint: { minimum: 60, maximum: 70 },
    heightConstraint: { minimum: 60, maximum: 70 },
  })),
);

nodes.push(
  ...props.knowledgeAreas.map((knowledgeArea) => ({
    id: knowledgeArea.uid,
    label: truncateText(knowledgeArea.title),
    title: `Knowledge Area
      Title: ${knowledgeArea.title}
      Description: ${knowledgeArea.description}`,
    color: '#c4b5fd',
    font: { size: 16 },
    widthConstraint: { minimum: 90, maximum: 100 },
    heightConstraint: { minimum: 90, maximum: 100 },
  })),
);

nodes = new DataSet(nodes);

let edges = [];

edges.push(
  ...props.coursesWithTopics.map((courseData) => ({
    id: courseData.TEACHES.uid,
    from: courseData.Course.uid,
    to: courseData.Topic.uid,
    label: `teaches`,
    title: `Teaches
      Level: ${courseData.TEACHES.level}
      Tools: ${courseData.TEACHES.tools ?? ''}
      Comments: ${courseData.TEACHES.comments ?? ''}`,
    value: props.levels.indexOf(courseData.TEACHES.level),
    // smooth: false,
    length: 300,
  })),
);

edges.push(
  ...props.knowledgeAreasWithTopics.map((item) => ({
    id: item.COVERS.uid,
    from: item.Topic.uid,
    to: item.KnowledgeArea.uid,
    label: `covers`,
    title: `Covers
      Level: ${item.COVERS.level}
      Tools: ${item.COVERS.tools ?? ''}
      Comments: ${item.COVERS.comments ?? ''}`,
    value: props.levels.indexOf(item.COVERS.level),
    length: 500,
  })),
);

edges.push(
  ...prereqData.map((prereqDataItem) => ({
    id: prereqDataItem.IS_PREREQUISITE_OF.uid,
    from: prereqDataItem.Course_from.uid,
    to: prereqDataItem.Course_to.uid,
    label: `is a prerequisite of`,
    // color: 'gray',
    length: 500,
    // dashes: true
  })),
);

edges = new DataSet(edges);

function toggleCourseVisibility(courseId: string, setVisibilityTo = null) {
  let isCourseVisible = nodes.get(courseId).hidden;

  if (typeof isCourseVisible === 'undefined') {
    isCourseVisible = false;
  }

  let shouldHideCourse;

  if (typeof setVisibilityTo === 'boolean') {
    shouldHideCourse = !setVisibilityTo;
  } else {
    shouldHideCourse = !isCourseVisible;
  }

  let nodeUpdates = [{ id: courseId, hidden: shouldHideCourse }];

  // commented because it might be confusing for the user to have Topics be hidden when the related course is hidden
  // hideRelatedTopics(nodeUpdates, courseId, shouldHideCourse);

  nodes.update(nodeUpdates);
}

function hideRelatedTopics(
  nodeUpdates: { hidden: boolean; id: string }[],
  courseId: string,
  shouldHideCourse: boolean,
) {
  nodeUpdates.push(
    ...props.coursesWithTopics
      .filter((item) => {
        if (
          selectedCourses.value.length === 0 ||
          selectedCourses.value.length === props.courses.length
        ) {
          return item.Course.uid === courseId;
        }

        return (
          item.Course.uid === courseId &&
          !isTopicAttachedToMultipleVisibleCourses(item.Topic.uid)
        );
      })
      .map((item) => ({ id: item.Topic.uid, hidden: shouldHideCourse })),
  );
}

function isTopicAttachedToMultipleVisibleCourses(topicId): boolean {
  let courseIdsTopicIsAttachedTo: string[] = props.coursesWithTopics
    .filter((item) => item.Topic.uid === topicId)
    .map((item) => item.Course.uid);

  if (courseIdsTopicIsAttachedTo.length < 2) return false;

  return (
    nodes.get({
      filter: function (node) {
        return (
          courseIdsTopicIsAttachedTo.includes(node.uid) &&
          (node.hidden === false || typeof node.hidden === 'undefined')
        );
      },
    }).length > 1
  );
}

function toggleRelationshipVisibility(
  relationshipData: Array<Object>,
  relationshipName: string,
) {
  let edgeUpdates = relationshipData.map((item) => ({
    id: item.uid,
    hidden: !selectedRelationships.value.includes(relationshipName),
  }));

  edges.update(edgeUpdates);
}

function truncateText(text: string, maxLength: Number = 20): string {
  return `${text.substring(0, 20)}${text.length > maxLength ? '...' : ''}`;
}

const data = {
  nodes: nodes,
  edges: edges,
};
const options = {
  edges: {
    arrows: 'to',
    // color: 'gray',
    arrowStrikethrough: false,
    scaling: {
      min: 1,
      max: 4,
      label: false,
    },
    font: { align: 'top', vadjust: -1 },
  },
  nodes: {
    shape: 'circle',
    borderWidth: 1.5
  },
};

onMounted(() => {
  const container = document.getElementById('graph-container');

  const network = new Network(container, data, options);
});
</script>

<template>
  <Head title="Visualization" />

  <div
    class="base-card flex h-[90vh] w-full flex-col space-y-2 px-4 py-4 text-sm md:w-11/12 md:text-base xl:px-10"
  >
    <div class="flex flex-wrap gap-x-5 gap-y-3 rounded-lg border p-3">
      <span class="font-semibold tracking-wide">Courses:</span>
      <PillDiv
        ><input
          v-model="selectAll"
          class="input-checkbox mr-2"
          type="checkbox"
          :value="true"
        />
        select all
      </PillDiv>
      <PillDiv v-for="course in courses">
        <input
          v-model="selectedCourses"
          @change="toggleCourseVisibility(course.uid)"
          class="input-checkbox mr-2"
          type="checkbox"
          :value="course.number"
        />
        {{ course.number }}
      </PillDiv>
    </div>
    <div class="flex flex-wrap gap-x-5 gap-y-3 rounded-lg border p-3">
      <span class="font-semibold tracking-wide">Relationships:</span>
      <PillDiv v-for="(relationshipData, relationshipName) in relationships">
        <input
          @change="
            toggleRelationshipVisibility(relationshipData, relationshipName)
          "
          class="input-checkbox mr-2"
          type="checkbox"
          v-model="selectedRelationships"
          :value="relationshipName"
        />
        {{ relationshipName }}
      </PillDiv>
    </div>
    <div
      id="graph-container"
      class="basis-full rounded-lg border bg-gray-100"
    ></div>
  </div>
</template>
