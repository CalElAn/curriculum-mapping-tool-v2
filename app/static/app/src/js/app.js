import './bootstrap';
import "../css/app.css";
import "flowbite";
import 'floating-vue/dist/style.css'

import { createApp, h } from "vue";
import { createInertiaApp, router } from "@inertiajs/vue3";
import "vite/modulepreload-polyfill";
import FloatingVue from 'floating-vue'

import Layout from './Layouts/Layout.vue';

const appName = import.meta.env.VITE_APP_NAME || "Curriculum Mapping Tool";

router.on("invalid", (event) => {
  if (event.detail.response.status === 403) event.preventDefault();
});

createInertiaApp({
  title: (title) => `${title} - ${appName}`,
  resolve: (name) => {
    const pages = import.meta.glob("./Pages/**/*.vue", { eager: true });

    let page = pages[`./Pages/${name}.vue`];

    page.default.layout = page.default.layout || Layout;

    return page;
  },
  setup({ el, App, props, plugin }) {
    const app = createApp({ render: () => h(App, props) }).use(plugin)
    .use(FloatingVue)
    // .use(ZiggyVue);

    // app.config.globalProperties.route = route; // not using the ZiggyVue plugin because deploying it in the GitHub action will be a bit problematic (I will have to install php and do a composer install)
    app.mount(el);
  },
  progress: {
    color: "#dc2626", // bg-red-600
  },
});
