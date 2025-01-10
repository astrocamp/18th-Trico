document.addEventListener("DOMContentLoaded", function () {
  const planSelect = document.getElementById("plan"); // 方案選擇下拉框
  const standardSection = document.getElementById("standard");
  const premiumSection = document.getElementById("premium");
  const termsSection = document.getElementById("terms-section");
  const placeholderButton = document.getElementById("placeholderButton"); // 假按鈕
  const linepayButton = document.getElementById("linepayButton"); // LINE Pay 按鈕
  const ecpayButton = document.getElementById("ecpayButton"); // 綠界按鈕
  const termsCheckbox = document.getElementById("terms");
  const paymentMethodSelect = document.getElementById("payment-method"); // 支付方式下拉框

  planSelect.addEventListener("change", togglePlanView);
  paymentMethodSelect.addEventListener("change", togglePaymentMethod);

  // 切換方案顯示
  function togglePlanView() {
    const selectedPlan = planSelect.value;
    if (selectedPlan === "standard") {
      standardSection.classList.remove("hidden");
      premiumSection.classList.add("hidden");
    } else if (selectedPlan === "premium") {
      premiumSection.classList.remove("hidden");
      standardSection.classList.add("hidden");
    }
  }

  // 切換支付方式並顯示對應按鈕
  function togglePaymentMethod() {
    const selectedPaymentMethod = paymentMethodSelect.value;
    const isAgreed = termsCheckbox.checked;

    if (isAgreed) {
      if (selectedPaymentMethod === "linepay") {
        placeholderButton.classList.add("hidden");
        linepayButton.classList.remove("hidden");
        ecpayButton.classList.add("hidden");
      } else if (
        ["credit_card", "atm", "barcode"].includes(selectedPaymentMethod)
      ) {
        placeholderButton.classList.add("hidden");
        linepayButton.classList.add("hidden");
        ecpayButton.classList.remove("hidden");
      } else {
        resetButtons();
      }
    } else {
      resetButtons();
    }
  }

  // 重置按鈕狀態為假按鈕
  function resetButtons() {
    placeholderButton.classList.remove("hidden");
    linepayButton.classList.add("hidden");
    ecpayButton.classList.add("hidden");
  }

  // 切換條款同意狀態
  termsCheckbox.addEventListener("change", function () {
    if (this.checked) {
      togglePaymentMethod();
    } else {
      resetButtons();
    }
  });

  linepayButton.addEventListener("click", initiateLinePay);

  // 發送 LINE Pay 支付請求
  async function initiateLinePay() {
    const plan = planSelect.value;
    const serviceId = "{{ service.id }}";

    // 發送支付請求到後端
    const response = await fetch(`/order/request/${serviceId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": "{{ csrf_token }}",
      },
      body: JSON.stringify({ plan: plan }),
    });

    // 解析後端返回的數據
    const data = await response.json();
    if (data.success) {
      window.location.href = data.payment_url;
    } else {
      alert("支付初始化失敗：" + data.message);
    }
  }

  // 初始狀態重置按鈕
  resetButtons();
});
