import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0b1020",
        panel: "#121932",
        panelSoft: "#182242",
        accent: "#66e3c4",
        accent2: "#7aa2ff",
        warn: "#ffb020",
      },
      boxShadow: {
        glow: "0 10px 30px rgba(102,227,196,0.12)",
      },
    },
  },
  plugins: [],
};

export default config;
