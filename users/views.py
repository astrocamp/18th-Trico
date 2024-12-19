from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


def register(request):
    if request.user.is_authenticated:
        return redirect("pages:home")

    if request.POST:
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "兩次密碼輸入不一致！")
            return redirect("users:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, f"使用者 {username} 已被註冊！")
            return redirect("users:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, f"信箱 {email} 已被註冊！")
            return redirect("users:register")

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "註冊成功!歡迎登入。")
        return redirect("users:login")
    return render(request, "users/register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("pages:home")

    if request.POST:
        user = authenticate(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user:
            login_user(request, user)
            return redirect("pages:home")
        else:
            messages.error(request, "登入失敗，請重新登入一次。")
            return redirect("users:login")
    return render(request, "users/login.html")


@require_POST
@login_required
def logout(request):
    logout_user(request)
    response = HttpResponse()
    response["HX-Redirect"] = "/"
    return response
    # return redirect("pages:home")

@login_required
def profile(request):
    if request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # Debug: 印出表單驗證錯誤
        if not user_form.is_valid():
            print("User Form Errors:", user_form.errors)

        if not profile_form.is_valid():
            print("Profile Form Errors:", profile_form.errors)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "個人資料已成功更新")
            return redirect("users:profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }

    return render(request, "users/profile.html", context)

@login_required
def user_dashboard(request):

    profile = request.user.profile

    if profile.is_freelancer:
        return render(request, "users/freelancer_dashboard.html")
    
    else:
        return render(request, "users/client_dashboard.html")

@login_required
def apply_freelancer(request):
    profile = request.user.profile

    if request.POST:
        profile.is_freelancer = True
        profile.freelancer_verified = True
        profile.save()
        return redirect("users:user_dashboard")

    return render(request, "users/apply_freelancer.html")


@login_required
def switch_role(request):
    profile = request.user.profile
    if profile.is_freelancer:
        profile.is_freelancer = False
        profile.save()
    else:
        profile.is_freelancer = True
        profile.save()
    
    return redirect("users:user_dashboard")