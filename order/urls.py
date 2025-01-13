from django.urls import path
from order import views

app_name = "order"
urlpatterns = [
    path("failed/", views.failed, name="failed"),
    path("successful/", views.successful, name="successful"),
    path("create/", views.create_order, name="create_order"),
    path("return/", views.ecpay_return, name="ecpay_return"),  
    path("result/", views.ecpay_result, name="ecpay_result"),  
    path("<int:service_id>/", views.payment_form_select, name="payment_form_select"),
    path("request/<int:service_id>/", views.request_payment, name='request_payment'),
    path("api/linepay_data/<int:service_id>/", views.get_linepay_data, name="get_linepay_data"),
    path("api/linepay_callback/", views.linepay_callback, name="linepay_callback"),


]
