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
    "align-text-bottom",
    "align-bottom",
    "item-end",
    "self-end",
    "pt-6",
    "pt-5",
    "sm:pl-3",
    "sm:text-xl",
    "sm:w-1/3",
    "",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
