/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.css",
    "./*/templates/**/*.html",
  ],
  theme: {
    extend: {
      minWidth: {
        "custom-xs": "390px", // 自定義最小寬度
      },
      screens: {
        xs: "40px", // 自定義斷點
        xxs: "380px", // 自定義斷點
        xxxs: "320px", // 自定義斷點
      },
    },
  },
  plugins: [require("daisyui")],
};
