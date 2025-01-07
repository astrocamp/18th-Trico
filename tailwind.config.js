/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.css",
    "./*/templates/**/*.html",
  ],
  safelist: [
    "sm:px-5",
    "w-1/4",
    "list-disc",
    "sm:gap-6",
    "hover:text-gray-800",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
