document.addEventListener("DOMContentLoaded", () => {
  const standardTab = document.getElementById("standard-tab");
  const premiumTab = document.getElementById("premium-tab");
  const standardSection = document.getElementById("standard");
  const premiumSection = document.getElementById("premium");

  standardTab.addEventListener("click", () => {
    standardSection.classList.remove("hidden");
    premiumSection.classList.add("hidden");
    standardTab.classList.add("border-b-2", "border-blue-500");
    premiumTab.classList.remove("border-b-2", "border-blue-500");
  });

  premiumTab.addEventListener("click", () => {
    premiumSection.classList.remove("hidden");
    standardSection.classList.add("hidden");
    premiumTab.classList.add("border-b-2", "border-blue-500");
    standardTab.classList.remove("border-b-2", "border-blue-500");
  });
});
