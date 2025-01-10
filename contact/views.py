from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactMessage


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )
            return redirect("contact:contact_success")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})


def contact_success_view(request):
    return render(request, "contact/contact_success.html")
