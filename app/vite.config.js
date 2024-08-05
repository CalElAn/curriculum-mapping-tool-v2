import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve, join } from "path";

export default defineConfig((mode) => {
  const env = loadEnv(mode, "..", "DJANGO_VITE_");

  const INPUT_DIR = "./static";
  const OUTPUT_DIR = "./static/app/dist";

  return {
    plugins: [vue()],
    root: resolve(INPUT_DIR),
    base: "/static/",
    resolve: {
      alias: {
        "@": resolve(INPUT_DIR, "app/src/js"),
      },
    },
    server: {
      host: true,
      port: env.DJANGO_VITE_DEV_SERVER_PORT,
      watch: {
        usePolling: true,
      },
    },
    build: {
      outDir: resolve(OUTPUT_DIR),
      // assetsDir: '',
      manifest: "manifest.json", // docs say it should be "manifest.json" but examples ay it should be "true". Check at build/preview time
      emptyOutDir: true,
      rollupOptions: {
        input: {
          app: join(INPUT_DIR, "/app/src/js/app.ts"),
        },
      },
    },
  };
});
