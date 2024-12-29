<template>
  <div>
    <h1 v-if="errorMessage">{{ errorMessage }}</h1>
    <p v-if="errorDetail">{{ errorDetail }}</p>
    <router-link to="/">Go Back Home</router-link>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  name: "NotFoundPage",
  setup() {
    const errorMessage = ref("");
    const errorDetail = ref("");

    onMounted(async () => {
      try {
        const response = await axios.get("/404", {
          headers: { Accept: "application/json" },
        });
        errorMessage.value = response.data.error;
        errorDetail.value = response.data.detail;
      } catch (error) {
        console.error("Error fetching JSON data:", error);
        errorMessage.value = "An unexpected error occurred.";
      }
    });

    return { errorMessage, errorDetail };
  },
};
</script>

<style scoped>
/* 添加樣式以美化錯誤頁面 */
</style>
