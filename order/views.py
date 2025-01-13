from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import Order
from datetime import datetime
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm
from services.models import Service
from django.conf import settings
from pathlib import Path
import hmac
import base64
import json
import uuid
import urllib.parse
import requests

# 第三方庫
import environ
from django.urls import reverse


MERCHANT_ID = settings.MERCHANT_ID
HASH_KEY = settings.HASH_KEY
HASH_IV = settings.HASH_IV
ECPAY_URL = settings.ECPAY_URL


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
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        selected_plan = request.POST.get("plan")
        payment_method = request.POST.get("payment_method")
        service = get_object_or_404(Service, id=service_id)

        # 動態設置金額
        if selected_plan == "standard":
            total_price = service.standard_price
        elif selected_plan == "premium":
            total_price = service.premium_price
        else:
            return JsonResponse({"error": "Invalid plan selected."}, status=400)
        valid_payment_methods = {
            "credit_card": "Credit",
            "atm": "ATM",
            # "googlepay": "GooglePay",等上線開通後才可啟用，測試環境不行
            "barcode": "BARCODE",
        }

        if payment_method not in valid_payment_methods:
            return JsonResponse(
                {"error": "Invalid payment method selected."}, status=400
            )

        # 建立訂單
        order = request.user.orders_as_client.create(
            service=service,
            total_price=total_price,
            payment_method=payment_method,
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
            "ReturnURL": request.build_absolute_uri(reverse("order:ecpay_return")),
            "OrderResultURL": request.build_absolute_uri(reverse("order:ecpay_result")),
            "ChoosePayment": valid_payment_methods[payment_method],
        }
        params["CheckMacValue"] = generate_check_mac_value(params, HASH_KEY, HASH_IV)

        # 傳遞至前端表單
        return render(
            request,
            "order/payment_form.html",
            {"ecpay_url": ECPAY_URL, "params": params},
        )
    return JsonResponse({"error": "Invalid request method."}, status=405)

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



def failed(request):
    return render(request, "order/order_failed.html")


def successful(request):
    return render(request, "order/order_successful.html")


# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()

def create_headers(payload, uri):
    channel_id = env("LINE_PAY_CHANNEL_ID")
    secret_key = env("LINE_PAY_CHANNEL_SECRET_KEY")

    nonce = str(uuid.uuid4())
    message = secret_key + uri + json.dumps(payload) + nonce
    signature = base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()).decode()

    return {
        "Content-Type": "application/json",
        "X-LINE-ChannelId": channel_id,
        "X-LINE-Authorization": signature,
        "X-LINE-Authorization-Nonce": nonce,
    }

def payment_form_select(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    selected_plan = request.GET.get("plan")  
    initial_data = {
        "selected_plan": selected_plan,
        "payment_method": None,
    }

    if request.method == "POST":
        form = OrderForm(request.POST, initial=initial_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_user = request.user
            order.service = service

            # 根據方案選擇設置總金額
            if form.cleaned_data["selected_plan"] == "standard":
                order.total_price = service.standard_price
            elif form.cleaned_data["selected_plan"] == "premium":
                order.total_price = service.premium_price
            else:
                form.add_error("selected_plan", "Invalid plan selected.")
                return render(
                    request,
                    "order/payment_form_select.html",
                    {"form": form, "service": service},
                )
            order.save()
            return redirect("order:successful", order_id=order.id)
        else:
            return render(
                request,
                "order/payment_form_select.html",
                {"form": form, "service": service, "selected_plan": selected_plan},
            )
    # GET 請求
    else:
        form = OrderForm(initial=initial_data)

    return render(
        request,
        "order/payment_form_select.html",
        {"form": form, "service": service, "selected_plan": selected_plan},
    )



# Line Pay
def get_linepay_data(request, service_id):
    """
    提供 LINE Pay 支付所需的數據
    """
    service = get_object_or_404(Service, id=service_id)
    data = {
        "service_id": service.id,
        "standard_price": service.standard_price,
        "premium_price": service.premium_price,
        "currency": "TWD",
    }
    return JsonResponse(data)

env = environ.Env()

@csrf_exempt
def request_payment(request, service_id):
    if request.method == "POST":
        data = json.loads(request.body)
        plan = data.get("plan")

        service = get_object_or_404(Service, id=service_id)
        amount = service.standard_price if plan == "standard" else service.premium_price

        payload = {
            "amount": amount,
            "currency": "TWD",
            "orderId": f"order_{uuid.uuid4()}",
            "packages": [
                {
                    "id": f"package_{uuid.uuid4()}",
                    "amount": amount,
                    "products": [{"name": f"{plan.capitalize()} Plan", "quantity": 1, "price": amount}],
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"https://{env('HOSTNAME')}/order/successful",
                "cancelUrl": f"https://{env('HOSTNAME')}/order/failed",
            },
        }

        uri = env("LINE_PAY_REQUEST_URL")
        headers = create_headers(payload, uri)
        response = requests.post(f"{env('LINE_PAY_SANDBOX_URL')}{uri}", headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if response_data["returnCode"] == "0000":
                return JsonResponse({"success": True, "payment_url": response_data["info"]["paymentUrl"]["web"]})
            return JsonResponse({"success": False, "message": response_data["returnMessage"]})
        return JsonResponse({"success": False, "message": f"Error: {response.status_code}"})

# 接收 LINE Pay 支付回調並更新訂單狀態
@csrf_exempt
def linepay_callback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        merchant_trade_no = data.get("orderId")
        status = data.get("transactionStatus")

        order = get_object_or_404(Order, merchant_trade_no=merchant_trade_no)
        if status == "SUCCESS":
            order.mark_as_paid()  # 使用狀態機改變狀態
        else:
            order.cancel_order()  # 使用狀態機改變狀態
        order.save()

        return JsonResponse({"message": "Payment processed successfully"})
