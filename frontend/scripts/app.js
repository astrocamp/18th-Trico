import "htmx.org";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router"; // 引入路由模組

// 創建 Vue 應用
const app = createApp(App);

// 使用路由和狀態管理
app.use(router);

// 掛載到 DOM
app.mount("#app");
