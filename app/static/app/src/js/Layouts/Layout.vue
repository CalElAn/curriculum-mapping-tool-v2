<script setup lang="ts">
import { Link, router } from "@inertiajs/vue3";
import { SquaresPlusIcon, TableCellsIcon } from "@heroicons/vue/24/outline";
import TabLink from "@/Components/TabLink.vue";
</script>

<template>
  <!-- button to open sidebar on mobile -->
  <button
    data-drawer-target="logo-sidebar"
    data-drawer-toggle="logo-sidebar"
    aria-controls="logo-sidebar"
    type="button"
    class="ms-3 mt-2 inline-flex items-center rounded-2xl p-2 text-sm text-gray-500 shadow hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600 sm:hidden"
  >
    <span class="sr-only">Open sidebar</span>
    <svg
      class="h-6 w-6"
      aria-hidden="true"
      fill="currentColor"
      viewBox="0 0 20 20"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        clip-rule="evenodd"
        fill-rule="evenodd"
        d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
      ></path>
    </svg>
  </button>

  <!-- Sidebar -->
  <aside
    id="logo-sidebar"
    class="fixed left-0 top-0 z-40 h-screen w-64 -translate-x-full bg-gray-50 transition-transform sm:translate-x-0 sm:p-2"
    aria-label="Sidebar"
  >
    <div
      class="h-full overflow-y-auto rounded-xl border bg-white px-3 py-4 dark:bg-gray-800"
    >
      <Link
        href="/"
        class="mb-5 flex items-center ps-2.5 text-lg font-semibold tracking-wide"
      >
        Curriculum Mapping Tool
        <!--        <span
                    class="self-center text-xl font-semibold whitespace-nowrap dark:text-white"
                    >Flowbite</span
                  >-->
      </Link>
      <ul class="mt-8 space-y-4 font-medium">
        <li>
          <Link
            :class="[
              $page.url.includes('data-entry')
                ? 'bg-red-200 font-semibold text-red-600'
                : 'font-medium hover:text-red-600 hover:underline',
            ]"
            :href="reverseUrl('app:courses.list')"
            class="flex w-full items-center justify-start gap-2 rounded-lg py-2 pl-3 tracking-wide"
          >
            <SquaresPlusIcon class="h-5 w-5 text-red-600" />
            Data Entry
          </Link>
        </li>
        <li>
          <Link
            :class="[
              $page.component.includes('GraphVisualization')
                ? 'bg-red-200 font-semibold text-red-600'
                : 'font-medium hover:text-red-600 hover:underline',
            ]"
            :href="reverseUrl('app:graph_visualization')"
            class="flex w-full items-center justify-start gap-2 rounded-lg py-2 pl-3 tracking-wide"
          >
            <!--            <svg
              xmlns="http://www.w3.org/2000/svg"
              version="1.1"
              viewBox="-5.0 -10.0 110.0 135.0"
              class="h-5 w-5 text-red-600"
            >
              <path
                d="m19.906 1c4.9766 0 9.4844 2.0195 12.75 5.2812s5.2812 7.7695 5.2812 12.75c0 4.082-1.3594 7.8516-3.6484 10.871l31.988 31.312c2.7852-2.2031 6.2344-3.6016 10-3.8477l1.2773-20.629c-3.6172-0.69141-6.8555-2.4609-9.3555-4.9609-3.2617-3.2656-5.2812-7.7695-5.2812-12.75 0-4.9766 2.0195-9.4844 5.2812-12.75 3.2656-3.2617 7.7695-5.2812 12.75-5.2812 4.9766 0 9.4844 2.0195 12.75 5.2812 3.2617 3.2656 5.2812 7.7695 5.2812 12.75 0 4.9766-2.0195 9.4844-5.2812 12.75-3.0039 3.0039-7.0625 4.9492-11.566 5.2422l-1.2773 20.625c3.6172 0.69141 6.8555 2.4609 9.3555 4.9609 3.2656 3.2617 5.2812 7.7695 5.2812 12.746 0 4.9766-2.0195 9.4844-5.2812 12.75-3.2617 3.2656-7.7695 5.2812-12.746 5.2812-4.9766 0-9.4844-2.0156-12.75-5.2812-2.3633-2.3633-4.0781-5.3828-4.8398-8.7617l-22.793 2.1914c-0.14844 4.7539-2.1328 9.0469-5.2695 12.184-3.2656 3.2617-7.7695 5.2812-12.75 5.2812-4.9766 0-9.4844-2.0195-12.75-5.2812-3.2617-3.2656-5.2812-7.7695-5.2812-12.75 0-4.9766 2.0195-9.4844 5.2812-12.75 3.2656-3.2617 7.7695-5.2812 12.75-5.2812 4.9766 0 9.4844 2.0195 12.75 5.2812 2.3633 2.3633 4.0742 5.3828 4.8398 8.7617l22.793-2.1914c0.12109-3.8672 1.4531-7.4258 3.6406-10.309l-31.988-31.312c-3.0703 2.4336-6.957 3.8867-11.18 3.8867-4.9766 0-9.4844-2.0195-12.75-5.2812-3.2617-3.2656-5.2812-7.7695-5.2812-12.75 0-4.9766 2.0195-9.4844 5.2812-12.75 3.2656-3.2617 7.7695-5.2812 12.75-5.2812z"
                fill="none"
                stroke="currentColor"
                stroke-width="6"
              />
            </svg>-->
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 100 125"
              class="h-5 w-5 text-red-600"
            >
              <g transform="translate(0,-952.36218)">
                <path
                  d="m 61,957.36218 c -5.49916,0 -10,4.50084 -10,10 0,3.4764 1.78745,6.55016 4.5,8.34375 l -4.90625,16.40625 c -1.45347,-0.47171 -2.98672,-0.75 -4.59375,-0.75 -3.47156,0 -6.67183,1.19425 -9.21875,3.1875 l -15.4375,-13 C 22.38633,980.08097 23,978.28846 23,976.36218 c 0,-4.94687 -4.05313,-9 -9,-9 -4.94688,0 -9,4.05313 -9,9 0,4.94688 4.05312,9 9,9 1.56112,0 3.02869,-0.417 4.3125,-1.125 l 15.65625,13.1875 C 32.10537,999.92423 31,1003.0175 31,1006.3622 c 0,3.407 1.16695,6.5391 3.09375,9.0625 l -10.15625,10.1875 c -1.9647,-1.4048 -4.35016,-2.25 -6.9375,-2.25 -6.60373,0 -12,5.3963 -12,12 0,6.6037 5.39627,12 12,12 6.60373,0 12,-5.3963 12,-12 0,-2.5873 -0.8452,-4.9728 -2.25,-6.9375 l 10.15625,-10.1563 c 2.5267,1.9359 5.67782,3.0938 9.09375,3.0938 5.55957,0 10.40929,-3.0792 13,-7.5938 l 14.15625,4.7188 c -0.10515,0.608 -0.15625,1.2381 -0.15625,1.875 0,6.0514 4.94856,11 11,11 6.05144,0 11,-4.9486 11,-11 0,-6.0515 -4.94856,-11 -11,-11 -4.00406,0 -7.51317,2.1872 -9.4375,5.4062 L 60.5,1010.0809 c 0.30669,-1.192 0.5,-2.4334 0.5,-3.7187 0,-1.4575 -0.23407,-2.8534 -0.625,-4.1875 l 14.875,-9.90626 c 1.65334,1.88599 4.06246,3.09375 6.75,3.09375 4.94688,0 9,-4.05312 9,-9 0,-4.94687 -4.05312,-9 -9,-9 -4.94687,0 -9,4.05313 -9,9 0,0.8119 0.10811,1.59397 0.3125,2.34375 l -14.59375,9.75 c -1.15135,-1.84108 -2.68877,-3.4309 -4.5,-4.625 l 5,-16.65625 c 0.58066,0.10599 1.17124,0.1875 1.78125,0.1875 5.49916,0 10,-4.50084 10,-10 0,-5.49916 -4.50084,-10 -10,-10 z m 0,4 c 3.3374,0 6,2.6626 6,6 0,3.3374 -2.6626,6 -6,6 -3.3374,0 -6,-2.6626 -6,-6 0,-3.3374 2.6626,-6 6,-6 z m -47,10 c 2.78511,0 5,2.21489 5,5 0,2.78512 -2.21489,5 -5,5 -2.78512,0 -5,-2.21488 -5,-5 0,-2.78511 2.21488,-5 5,-5 z m 68,10 c 2.78512,0 5,2.21489 5,5 0,2.78512 -2.21488,5 -5,5 -2.78511,0 -5,-2.21488 -5,-5 0,-2.78511 2.21489,-5 5,-5 z m -36,14 c 6.09883,0 11,4.90122 11,11.00002 0,6.0988 -4.90117,11 -11,11 -6.09882,0 -11,-4.9012 -11,-11 0,-6.0988 4.90118,-11.00002 11,-11.00002 z m 38,18.00002 c 3.88968,0 7,3.1103 7,7 0,3.8897 -3.11032,7 -7,7 -3.88968,0 -7,-3.1103 -7,-7 0,-3.8897 3.11032,-7 7,-7 z m -67,14 c 4.44197,0 8,3.558 8,8 0,4.442 -3.55803,8 -8,8 -4.44197,0 -8,-3.558 -8,-8 0,-4.442 3.55803,-8 8,-8 z"
                  fill="currentColor"
                  stroke="currentColor"
                />
              </g>
            </svg>
            Graph
          </Link>
        </li>
        <li>
          <Link
            :class="[
              $page.url.includes('data-entry')
                ? 'bg-red-200 font-semibold text-red-600'
                : 'font-medium hover:text-red-600 hover:underline',
            ]"
            :href="reverseUrl('app:matrix')"
            class="flex w-full items-center justify-start gap-2 rounded-lg py-2 pl-3 tracking-wide"
          >
            <TableCellsIcon class="h-5 w-5 text-red-600" />
            Matrix
          </Link>
        </li>
      </ul>
    </div>
  </aside>

  <div class="min-h-screen bg-gray-50 px-4 py-2 sm:ml-64">
    <div class="md:w-11/12 space-y-6">
      <header
        class="w-full rounded-xl bg-white px-4 py-2 text-sm shadow"
      >
        <nav class="flex w-full items-center justify-end" aria-label="Global">
          <!--        <div class="h-9 w-9 rounded-full bg-gray-200" aria-hidden="true"></div>-->

          <button
            id="dropdownAvatarNameButton"
            data-dropdown-toggle="dropdownAvatarName"
            class="flex items-center rounded-full pe-1 text-sm font-medium text-gray-900 hover:text-blue-600 focus:ring-4 focus:ring-gray-100 dark:text-white dark:hover:text-blue-500 dark:focus:ring-gray-700 md:me-0"
            type="button"
          >
            <span class="sr-only">Open user menu</span>
            <div
              class="me-2 h-8 w-8 rounded-full bg-gray-200"
              alt="user photo"
            ></div>
            <!--            {{ $page.props.auth.user.name }}-->
            <svg
              class="ms-3 h-2.5 w-2.5"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 10 6"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 1 4 4 4-4"
              />
            </svg>
          </button>

          <!-- Dropdown menu -->
          <div
            id="dropdownAvatarName"
            class="z-10 hidden w-44 divide-y divide-gray-100 rounded-lg bg-white shadow dark:divide-gray-600 dark:bg-gray-700"
          >
            <!--          <div class="px-4 py-3 text-sm text-gray-900 dark:text-white">
              <div class="font-medium">Pro User</div>
              <div class="truncate">name@flowbite.com</div>
            </div>-->
            <ul
              class="py-2 text-sm text-gray-700 dark:text-gray-200"
              aria-labelledby="dropdownInformdropdownAvatarNameButtonationButton"
            >
              <li>
                <a
                  href="#"
                  class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white"
                >Profile</a
                >
                <!-- TODO Profile link and page -->
              </li>
            </ul>
            <div class="py-2">
              <Link
                @click="router.post(reverseUrl('logout'))"
                as="button"
                type="button"
                href="#"
                class="block w-full px-4 py-2 text-start text-sm text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-gray-600 dark:hover:text-white"
              >Sign out
              </Link>
            </div>
          </div>
        </nav>
      </header>
      <div
        v-if="$page.url.includes('data-entry')"
        class="border-b border-gray-200 text-center text-base font-medium text-gray-500 dark:border-gray-700 dark:text-gray-400"
      >
        <ul class="-mb-px flex flex-wrap">
          <li class="me-2">
            <TabLink title="Courses" activeIfIncludes="courses" />
          </li>
          <li class="me-2">
            <TabLink title="Topics" activeIfIncludes="topics" />
          </li>
          <li class="me-2">
            <TabLink title="Knowledge Areas" activeIfIncludes="knowledge-areas" />
          </li>
        </ul>
      </div>
      <slot />
    </div>
  </div>
</template>
