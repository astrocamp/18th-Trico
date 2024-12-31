from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Order
from datetime import datetime
import hashlib
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from django.contrib.auth.decorators import login_required

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
    service_id = request.GET.get("service_id", 1)  # 預設為 1
    total_price = 1000.0  # TODO:測試金額

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
        "ReturnURL": "http://127.0.0.1:8000/order/return/",  # TODO:部署要換
        "OrderResultURL": "http://127.0.0.1:8000/order/result/",  # TODO:部署要換
        "ChoosePayment": "Credit",
    }
    params["CheckMacValue"] = generate_check_mac_value(params, HASH_KEY, HASH_IV)

    # 將參數發送到前端表單，讓用戶跳轉至綠界支付頁面
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
