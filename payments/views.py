from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def payment_page(request, id):
    return render(request, "services/payment_form.html", {"service_id": id})
