/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.css",
    "./*/templates/**/*.html",
  ],
  safelist: [
    "w-64",
    "h-64",
    "bg-gradient-to-r",
    "from-blue-500",
    "to-green-500",
    "hover:bg-gradient-to-l",
    "hover:from-pink-500",
    "hover:to-purple-500",
    "hover:from-sky-100",
    "hover:to-sky-400",
    "transition-all",
    "duration-300",
    "ease-in-out",
    "text-center",
    "text-white",
    "pt-24",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
