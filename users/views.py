from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST


# Create your views here.


def register(request):
    if request.POST:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            # messages.success(request, "註冊成功")
            return redirect("pages:home")
        else:
            return HttpResponse("註冊失敗")

    return render(request, "users/register.html")


def login(request):
    if request.POST:
        # 驗證
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user is not None:
            login_user(request, user)
            messages.success(request, "登入成功")
            return redirect("pages:home")
        else:
            messages.success(request, "登入失敗")
            return redirect("users:login")
    return render(request, "users/login.html")


@require_POST
@login_required
def logout(request):
    logout_user(request)
    messages.success(request, "已登出")
    return redirect("pages:home")
