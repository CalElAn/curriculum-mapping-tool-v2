<template>
  <Head title="Channel Performance Detail" />
  <div class="base-card p-2">
    <p class="form-title bg-blue-100 p-1 text-center">
      Channel Performance Detail
    </p>
  </div>
  <div class="base-card mt-6 w-full px-4 py-4 text-sm md:text-base xl:px-10">
    <form @submit.prevent="submit" class="space-y-6 mt-12">
      <div class="flex flex-wrap gap-x-6 gap-y-4 items-center">
        <div>
          <label for="" class="label block">Date range</label>
<!--          <VueDatePicker class="mt-1" v-model="dateRange" range></VueDatePicker>-->
        </div>
        <div>
          <label for="" class="label block">Group by</label>
          <select required v-model="groupBy" class="select mt-1">
            <option v-for="item in groupByOptions" :value="item">
              {{ capitalize(item) }}
            </option>
          </select>
        </div>
        <div>
          <label class="label block">Client</label>
          <select required v-model="client" class="select mt-1">
            <option selected disabled value="">- select a client -</option>
            <option v-for="item in clients">{{ item }}</option>
          </select>
        </div>
      </div>
      <div class="flex items-center gap-4">
        <button
          type="submit"
          class="inline-flex flex-wrap items-center justify-center gap-1 rounded-lg border border-red-600 px-2 py-1 tracking-wide text-red-600 shadow-sm hover:bg-red-100 disabled:opacity-50"
        >
          Submit
        </button>
        <button
          type="button"
          class="inline-flex flex-wrap items-center justify-center gap-1 rounded-lg border border-red-600 px-2 py-1 tracking-wide text-red-600 shadow-sm hover:bg-red-100 disabled:opacity-50"
        >
          Export
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { Head } from "@inertiajs/vue3";
import { onMounted, ref } from "vue";
import capitalize from "lodash/capitalize";

// const props = defineProps({
//   clients: Array,
// });

const clients = ["betus"];

const groupByOptions = ["day", "week", "month"];

const dateRange = ref();
const groupBy = ref(groupByOptions[0]);
const client = ref("");

const columns = ref([
  {
    data: "date",
    title: "Date",
  },
  {
    data: "day",
    title: "Day",
  },
  {
    data: "ecpm",
    title: "eCPM",
    render: ["number", ",", ".", 2, "$"],
  },
  {
    data: "sum_total_signups",
    title: "Total Signups",
  },
  {
    data: "prospecting_client_signup_ecpa",
    title: "Prospecting CL Signup eCPA",
    render: ["number", ",", ".", 2, "$"],
  },
  {
    data: "retargeting_client_signup_ecpa",
    title: "Retargeting CL Signup eCPA",
    render: ["number", ",", ".", 2, "$"],
  },
  {
    data: "signup_cvrm",
    title: "Signup CVRM",
    render: ["number", ",", ".", 2, "", "%"],
  },
  {
    data: "sum_total_client_spend",
    title: "Total Client Spend",
    render: ["number", ",", ".", 2, "$"],
  },
]);
const data = ref([]);

function submit() {
  axios.get("get_channel_performance_report_data").then((response) => {
    console.log(response.data);
    // columns.value = response.data.table_columns;
    data.value = response.data.table_data;
  });
}

onMounted(() => {
  const startDate = new Date();
  const endDate = new Date(new Date().setDate(startDate.getDate() + 7));
  dateRange.value = [startDate, endDate];
});
</script>

