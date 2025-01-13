import "htmx.org";
import Alpine from "alpinejs";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 引入路由模組
import { all } from "axios";

// 創建 Vue 應用
const app = createApp(App);

// 使用路由和狀態管理
app.use(router);

// 取得 data-page 的值，改為從 <div> 中讀取
const pageElement = document.querySelector("[data-page]");
const pageName = pageElement ? pageElement.dataset.page : null;

if (pageName === "switching_tab") {
  import("../scripts/switching_tab.js").then((module) => {
    module.init();
  });
} else if (pageName === "toggling_plan") {
  import("../scripts/toggling_plan.js").then((module) => {
    module.init();
  });
} else if (pageName === "toggling_buttons") {
  import("../scripts/toggling_buttons.js").then((module) => {
    module.init();
  });
} else if (pageName === "plan_order_form") {
  import("./plan_order_form.js").then((module) => {
    module.init();
  });
} else if (pageName === "like_button") {
  import("../scripts/like_button.js").then((module) => {
    module.init();
  });
}

// 掛載到 DOM
app.mount("#app");
window.Alpine = Alpine;
Alpine.start();
