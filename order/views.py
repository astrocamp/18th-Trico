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
from notification.utils import send_notification

# 第三方庫
import environ
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

MERCHANT_ID = settings.MERCHANT_ID
HASH_KEY = settings.HASH_KEY
HASH_IV = settings.HASH_IV
ECPAY_URL = settings.ECPAY_URL


# 按照綠界的規範處理參數
def generate_check_mac_value(params, hash_key, hash_iv):
    sorted_params = sorted(params.items())
    raw_str = "&".join([f"{key}={value}" for key, value in sorted_params])
    raw_str = f"HashKey={hash_key}&{raw_str}&HashIV={hash_iv}"
    encoded_str = urllib.parse.quote_plus(raw_str).lower()
    return hashlib.md5(encoded_str.encode("utf-8")).hexdigest().upper()


# 建立綠界訂單
@login_required
def create_order(request):
    if request.method == "POST":
        try:
            # 確保必要參數存在
            service_id = request.POST.get("service_id")
            selected_plan = request.POST.get("plan")
            payment_method = request.POST.get("payment_method")

            if not all([service_id, selected_plan, payment_method]):
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # 驗證服務存在
            service = get_object_or_404(Service, id=service_id)
            client_user = request.user

            # 驗證計劃和付款方式
            if selected_plan not in ["standard", "premium"]:
                return JsonResponse({"error": "Invalid plan selected."}, status=400)

            valid_payment_methods = {
                "credit_card": "Credit",
                "atm": "ATM",
                "barcode": "BARCODE",
            }

            if payment_method not in valid_payment_methods:
                return JsonResponse(
                    {
                        "error": f"Invalid payment method. Allowed methods: {list(valid_payment_methods.keys())}"
                    },
                    status=400,
                )

            # 設置金額
            total_price = (
                service.standard_price
                if selected_plan == "standard"
                else service.premium_price
            )

            if total_price <= 0:
                return JsonResponse({"error": "Invalid total price."}, status=400)

            # 建立訂單
            order = request.user.orders_as_client.create(
                service=service,
                total_price=total_price,
                payment_method=payment_method,
            )

            # 發送通知給接案者
            send_notification(
                actor=client_user,
                recipient=service.freelancer_user,
                verb="下訂了您的服務",
                description=f"用戶 {client_user.username} 購買了您的服務：'{service.title}'。",
                target_service=service,
            )

            # 使用狀態機將狀態更新為 `paid`
            if order.status == "pending":
                order.mark_as_paid()  # 狀態機轉換
                order.save()

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
                "OrderResultURL": request.build_absolute_uri(
                    reverse("order:ecpay_result")
                ),
                "ChoosePayment": valid_payment_methods[payment_method],
            }

            # 加入檢查碼
            params["CheckMacValue"] = generate_check_mac_value(
                params, HASH_KEY, HASH_IV
            )

            # 回傳前端頁面
            return render(
                request,
                "order/payment_form.html",
                {"ecpay_url": ECPAY_URL, "params": params},
            )

        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return JsonResponse({"error": "Internal server error."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def ecpay_return(request):
    if request.method == "POST":
        data = request.POST.dict()

        # 模擬測試環境返回成功的 RtnCode
        if settings.DEBUG:  # 僅在測試環境下生效
            data["RtnCode"] = "1"

        print("Received Data with Mocked RtnCode:", data)

        # 以下保留你的邏輯
        received_mac = data.get("CheckMacValue")
        if "CheckMacValue" in data:
            del data["CheckMacValue"]

        generated_mac = generate_check_mac_value(data, HASH_KEY, HASH_IV)
        if received_mac == generated_mac:
            merchant_trade_no = data.get("MerchantTradeNo")
            order = get_object_or_404(Order, merchant_trade_no=merchant_trade_no)
            if data["RtnCode"] == "1":
                order.mark_as_paid()
                return HttpResponse("OK")
            else:
                return HttpResponse("Payment Failed")
        else:
            return HttpResponse("CheckMacValue Failed")
    return HttpResponse("Invalid request method.")


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
    signature = base64.b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()

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
                    "products": [
                        {
                            "name": f"{plan.capitalize()} Plan",
                            "quantity": 1,
                            "price": amount,
                        }
                    ],
                }
            ],
            "redirectUrls": {
                "confirmUrl": f"https://{env('HOSTNAME')}/order/successful",
                "cancelUrl": f"https://{env('HOSTNAME')}/order/failed",
            },
        }

        uri = env("LINE_PAY_REQUEST_URL")
        headers = create_headers(payload, uri)
        response = requests.post(
            f"{env('LINE_PAY_SANDBOX_URL')}{uri}", headers=headers, json=payload
        )

        if response.status_code == 200:
            response_data = response.json()
            if response_data["returnCode"] == "0000":
                return JsonResponse(
                    {
                        "success": True,
                        "payment_url": response_data["info"]["paymentUrl"]["web"],
                    }
                )
            return JsonResponse(
                {"success": False, "message": response_data["returnMessage"]}
            )
        return JsonResponse(
            {"success": False, "message": f"Error: {response.status_code}"}
        )


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
