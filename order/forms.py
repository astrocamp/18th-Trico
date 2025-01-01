from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "selected_plan",
            "payment_method",
        ]
        widgets = {
            "selected_plan": forms.RadioSelect(attrs={"class": "plan-select"}),
            "payment_method": forms.Select(attrs={"class": "payment-method"}),
        }
        labels = {
            "selected_plan": "選擇方案",
            "payment_method": "支付方式",
        }
