import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        mastery: {
          beginner: "#ef4444",
          learning: "#eab308",
          proficient: "#22c55e",
          mastered: "#3b82f6",
        },
      },
    },
  },
  plugins: [],
};
export default config;
