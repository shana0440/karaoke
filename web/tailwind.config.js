/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        "dark-slate-grey": "#37383C",
        charcoal: "#46474B",
        "sonic-silver": "#545659",
        "light-grey": "#C3C4C5",
        "alice-blue": "#FBFCFF",
        "mint-cream": "#FBFCF5",
        jet: "#303134",
        "outer-space": "#292A2D",
        gunmetal: "#26272A",
        "dodger-blue": "#2472EC",
        "cod-gray": "#1B1B1D",
        "purple-taupe": "#505156",
        "transparent-black": "rgba(0,0,0,.5)",
        "black-coral": "#3B3C3E",
        "transparent-red": "rgba(21,22,23,.5)",
        bastille: "#353639",
        "terracotta-red": "#BB3333",
        "sky-blue": "#4D90FE",
      }
    },
  },
  plugins: [],
}

