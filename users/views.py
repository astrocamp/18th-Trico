from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from comments.models import Comment
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
            # next是用來在登入後跳轉到指定URL的參數
            next_url = request.GET.get("next")  
            if next_url: 
                return redirect(next_url) 
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


@login_required
def profile(request):
    if request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

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

    context = {"user_form": user_form, "profile_form": profile_form}

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


# 忘記密碼
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = "/users/password_reset_done/"
    extra_context = {
        "protocol": settings.PROTOCOL,
        "domain": settings.DEFAULT_DOMAIN,
    }

    # 覆蓋郵件發送邏輯，避免重複發送郵件
    def form_valid(self, form):
        email = form.cleaned_data["email"]

        for user in form.get_users(email):
            context = {
                "email": email,
                "domain": settings.DEFAULT_DOMAIN,
                "protocol": settings.PROTOCOL,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            subject = render_to_string(self.subject_template_name, context).strip()
            html_message = render_to_string(self.email_template_name, context)

            # 發送郵件
            email_msg = EmailMessage(
                subject=subject,
                body=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            email_msg.content_subtype = "html"
            email_msg.send()

        # 不再調用的郵件發送邏輯
        return super(auth_views.PasswordResetView, self).form_valid(form)


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = "/users/reset_done/"


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"


def switch_role(request):
    profile = request.user.profile
    if profile.is_freelancer:
        profile.is_freelancer = False
        profile.save()
    else:
        profile.is_freelancer = True
        profile.save()

    return redirect("users:user_dashboard")


@login_required
def feedback_view(request):
    profile = request.user.profile
    if profile.is_freelancer: 
        comments_received = Comment.objects.filter(
            service__freelancer_user=request.user, is_deleted=False
        ).select_related("user", "service")
        context = {
            "comments_received": comments_received,
            "role": "freelancer",  
        }
    else:  
        comments_given = Comment.objects.filter(
            user=request.user, is_deleted=False
        ).select_related("service", "service__freelancer_user")
        context = {
            "comments_given": comments_given,
            "role": "client",  
        }

    return render(request, "users/feedback.html", context)



# 個人首頁
def information(request, username):
    user = get_object_or_404(User, username=username)  
    return render(request, "users/information.html", {"user": user})


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'a_users/profile.html', {'profile':profile})