// JavaScript for toggling management buttons
document
  .getElementById("toggle-management-btn")
  .addEventListener("click", function () {
    const managementButtons = document.querySelectorAll(".management-buttons");
    managementButtons.forEach((buttonGroup) => {
      if (buttonGroup.classList.contains("hidden")) {
        buttonGroup.classList.remove("hidden");
      } else {
        buttonGroup.classList.add("hidden");
      }
    });
  });
