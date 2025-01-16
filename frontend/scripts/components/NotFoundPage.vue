<template>
    <div class="bg-white min-h-screen flex flex-col items-center justify-center text-center">
        <!-- Error Number -->
        <h1 class="text-9xl font-extrabold text-gray-900">
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#ff1dbf] via-[#004fff] to-[#42d3d8]">
                {{ displayedErrorMessage }}
            </span>
        </h1>
        <!-- Error Message -->
        <p class="text-2xl font-bold text-gray-800 mt-4 uppercase tracking-wide">{{ displayedErrorDetail }}</p>
        <!-- Buttons -->
        <div class="flex mt-6 space-x-4">
            <a href="/"
                class="px-6 py-3 text-sm font-medium bg-transparent border border-[#ff1dbf] text-[#ff1dbf] hover:bg-[#ff1dbf] hover:text-white rounded transition-all">
                返回首頁
            </a>
            <a href="/contact/"
                class="px-6 py-3 text-sm font-medium bg-transparent border border-[#ff1dbf] text-[#ff1dbf] hover:bg-[#ff1dbf] hover:text-white rounded transition-all">
                聯絡我們
            </a>
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

        const displayedErrorMessage = ref("");
        const displayedErrorDetail = ref("");

        const typeEffect = (source, target, speed) => {
            let currentIndex = 0;
            const interval = setInterval(() => {
                if (currentIndex < source.value.length) {
                    target.value += source.value[currentIndex];
                    currentIndex++;
                } else {
                    clearInterval(interval); // 完成後清除計時器
                }
            }, speed);
        }

        onMounted(async () => {
            try {
                const response = await axios.get("/api/404/", {
                    headers: { Accept: "application/json" },
                });
                errorMessage.value = String(response.data.status_code) || "Error not specified.";
                errorDetail.value = response.data.detail || "No additional details provided.";
            } catch (error) {
                console.error("Error fetching JSON data:", error.response || error.message);
                if (error.response) {
                    // 從錯誤響應中提取數據
                    errorMessage.value = String(error.response.data.status_code) || "Error not specified.";
                    errorDetail.value = error.response.data.detail || "No additional details provided.";
                } else {
                    errorMessage.value = "An unexpected error occurred.";
                    errorDetail.value = "No additional details available.";
                }
            }

            // 執行打字效果 (標題和內容逐字出現)
            typeEffect(errorMessage, displayedErrorMessage, 100); // 每個字母 100ms
            setTimeout(() => {
                typeEffect(errorDetail, displayedErrorDetail, 50); // 每個字母 50ms
            }, 1000); // 等待 1 秒後開始顯示細節
        });

        return { displayedErrorMessage, displayedErrorDetail };
    },
};
</script>

<style scoped>
h1::after {
    content: "|";
    animation: blink 0.5s step-end infinite;
}

@keyframes blink {
    50% {
        opacity: 0;
    }
}
</style>