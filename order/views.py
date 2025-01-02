from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Order
from datetime import datetime
import hashlib
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from services.models import Service

# 綠界金流設定
MERCHANT_ID = "3002607"
HASH_KEY = "pwFHCqoQZGmho4w6"
HASH_IV = "EkRm7iFT261dpevs"
ECPAY_URL = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"


# 按照綠界的規範處理參數
def generate_check_mac_value(params, hash_key, hash_iv):
    sorted_params = sorted(params.items())
    raw_str = "&".join([f"{key}={value}" for key, value in sorted_params])
    raw_str = f"HashKey={hash_key}&{raw_str}&HashIV={hash_iv}"
    # 進行 URL 編碼並轉為小寫
    encoded_str = urllib.parse.quote_plus(raw_str).lower()
    # 計算 MD5 並轉為大寫
    return hashlib.md5(encoded_str.encode("utf-8")).hexdigest().upper()


# 建立訂單
@login_required
def create_order(request):
    client_user_id = request.user.id
    service_id = request.GET.get("service_id")  # 確保從前端獲取 service_id
    selected_plan = request.GET.get("plan")  # 獲取前端傳入的方案
    service = get_object_or_404(Service, id=service_id)

    # 動態設置金額
    if selected_plan == "standard":
        total_price = service.standard_price
    elif selected_plan == "premium":
        total_price = service.premium_price
    else:
        return JsonResponse({"error": "Invalid plan selected."}, status=400)

    # 建立訂單
    order = Order.objects.create(
        client_user_id=client_user_id,
        service_id=service_id,
        total_price=total_price,
        status="Pending",
        payment_method="CreditCard",
    )

    # 綠界金流參數
    params = {
        "MerchantID": MERCHANT_ID,
        "MerchantTradeNo": order.merchant_trade_no,
        "MerchantTradeDate": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "PaymentType": "aio",
        "TotalAmount": int(order.total_price),
        "TradeDesc": "Payment for Order",
        "ItemName": f"Order {order.id}",
        "ReturnURL": "http://127.0.0.1:8000/order/return/",
        "OrderResultURL": "http://127.0.0.1:8000/order/result/",
        "ChoosePayment": "Credit",
    }
    params["CheckMacValue"] = generate_check_mac_value(params, HASH_KEY, HASH_IV)

    # 傳遞至前端表單
    return render(
        request, "order/payment_form.html", {"ecpay_url": ECPAY_URL, "params": params}
    )


@csrf_exempt
def ecpay_return(request):
    if request.method == "POST":
        data = request.POST.dict()
        check_mac = data.pop("CheckMacValue", None)

        if check_mac == generate_check_mac_value(data, HASH_KEY, HASH_IV):
            merchant_trade_no = data.get("MerchantTradeNo")
            order_id = int(merchant_trade_no.replace("ORDER", ""))
            order = get_object_or_404(Order, id=order_id)
            if data.get("RtnCode") == "1":  # 成功付款
                order.status = "Paid"
                order.save()
                return HttpResponse("OK")
        return HttpResponse("CheckMacValue Failed")


@csrf_exempt
def ecpay_result(request):
    return render(request, "order/order_successful.html")


def order(request):
    pass


def failed(request):
    return render(request, "order/order_failed.html")


def successful(request):
    return render(request, "order/order_successful.html")


def payment_form_select(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    selected_plan = request.GET.get("plan")  # 獲取選擇的方案

    # 初始表單數據，包括選擇的方案和預設支付方式
    initial_data = {
        "selected_plan": selected_plan,
        "payment_method": None,  # 默認支付方式為None
    }

    if request.method == "POST":
        form = OrderForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_user = request.user
            order.service = service
            # 設置總金額根據選擇的方案
            if form.cleaned_data["selected_plan"] == "standard":
                order.total_price = service.standard_price
            elif form.cleaned_data["selected_plan"] == "premium":
                order.total_price = service.premium_price
            else:
                # 如果方案不正確，返回表單錯誤
                form.add_error("selected_plan", "Invalid plan selected.")
                return render(
                    request,
                    "order/payment_form_select.html",
                    {"form": form, "service": service},
                )

            order.save()
            # 成功保存後，重定向到訂單成功頁面
            return redirect("order:successful", order_id=order.id)
    else:
        form = OrderForm(initial=initial_data)

    return render(
        request,
        "order/payment_form_select.html",
        {"form": form, "service": service, "selected_plan": selected_plan},
    )
