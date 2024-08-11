import defaultTheme from "tailwindcss/defaultTheme";
import forms from "@tailwindcss/forms";

/** @type {import("tailwindcss").Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./static/app/src/js/**/*.vue",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Figtree", ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [forms, require("flowbite/plugin")],
};
