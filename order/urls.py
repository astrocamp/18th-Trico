from django.urls import path
from order import views

app_name = "order"
urlpatterns = [
    path("failed/", views.failed, name="order_failed"),
    path("successful/", views.successful, name="order_successful"),
    path("create/", views.create_order, name="create_order"),
    path("return/", views.ecpay_return, name="ecpay_return"),
    path("result/", views.ecpay_result, name="ecpay_result"),
]
