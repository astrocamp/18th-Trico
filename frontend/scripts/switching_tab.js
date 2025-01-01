document.addEventListener("DOMContentLoaded", function () {
  const standardTab = document.getElementById("standard-tab");
  const premiumTab = document.getElementById("premium-tab");
  const standardSection = document.getElementById("standard");
  const premiumSection = document.getElementById("premium");

  standardTab.addEventListener("click", function () {
    standardSection.classList.remove("hidden");
    premiumSection.classList.add("hidden");
    standardTab.classList.add("border-blue-500", "text-blue-700");
    premiumTab.classList.remove("border-blue-500", "text-blue-700");
  });

  premiumTab.addEventListener("click", function () {
    premiumSection.classList.remove("hidden");
    standardSection.classList.add("hidden");
    premiumTab.classList.add("border-blue-500", "text-blue-700");
    standardTab.classList.remove("border-blue-500", "text-blue-700");
  });
});
