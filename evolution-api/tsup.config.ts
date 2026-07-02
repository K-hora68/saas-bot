import { cpSync } from "node:fs";
import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["src/index.ts"],

  outDir: "dist",

  format: ["cjs", "esm"],

  splitting: false,

  sourcemap: true,

  clean: true,

  minify: true,

  dts: true,

  loader: {
    ".json": "file",
    ".yml": "file",
  },

  onSuccess: async () => {
    cpSync("src/utils/translations", "dist/translations", {
      recursive: true,
    });
  },
});