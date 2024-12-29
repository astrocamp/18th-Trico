<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="text-center">
      <h1 class="text-6xl font-bold mb-4 text-gray-800">{{ errorMessage }}</h1>
      <p class="text-xl mb-4 text-gray-600">
        {{ errorDetail }}
      </p>
      <div class="space-x-2">
        <a href="/" class="btn btn-primary">
          Go Back Home
        </a>
        <a href="/contact" class="btn btn-secondary">
          Contact Us
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
    name: "NotFoundPage",
    setup() {
        const errorMessage = ref("Loading...");
        const errorDetail = ref("Fetching error details...");

        onMounted(async () => {
            try {
                const response = await axios.get("/api/404/", {
                    headers: { Accept: "application/json" },
                });
                errorMessage.value = response.data.status_code || "Error not specified.";
                errorDetail.value = response.data.detail || "No additional details provided.";
            } catch (error) {
                console.error("Error fetching JSON data:", error.response || error.message);
                if (error.response) {
                    // 從錯誤響應中提取數據
                    errorMessage.value = error.response.data.status_code || "Error not specified.";
                    errorDetail.value = error.response.data.detail || "No additional details provided.";
                } else {
                    errorMessage.value = "An unexpected error occurred.";
                    errorDetail.value = "No additional details available.";
                }
            }
        });

        return { errorMessage, errorDetail };
    },
};
</script>