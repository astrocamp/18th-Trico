document.addEventListener("DOMContentLoaded", function () {
  const planSelect = document.getElementById("plan");
  const standardSection = document.getElementById("standard");
  const premiumSection = document.getElementById("premium");

  // 切換方案顯示
  planSelect.addEventListener("change", function () {
    if (this.value === "standard") {
      standardSection.classList.remove("hidden");
      premiumSection.classList.add("hidden");
    } else if (this.value === "premium") {
      premiumSection.classList.remove("hidden");
      standardSection.classList.add("hidden");
    }
  });

  // 初始化顯示對應方案
  function initializePlanView() {
    const selectedPlan = planSelect.value;
    if (selectedPlan === "standard") {
      standardSection.classList.remove("hidden");
      premiumSection.classList.add("hidden");
    } else if (selectedPlan === "premium") {
      premiumSection.classList.remove("hidden");
      standardSection.classList.add("hidden");
    }
  }

  initializePlanView();
});