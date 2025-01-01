  document
  .getElementById("toggle-premium-plan-btn")
  .addEventListener("click", function () {
    const premiumContainer = document.getElementById("premium-plan-container");
    if (premiumContainer.classList.contains("hidden")) {
      premiumContainer.classList.remove("hidden");
      this.textContent = "收回專業方案";
    } else {
      premiumContainer.classList.add("hidden");
      this.textContent = "新增專業方案";
    }
  });


      