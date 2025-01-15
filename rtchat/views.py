from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from urllib.parse import unquote
from .models import ChatGroup
from .forms import ChatmessageCreateForm
from django.core.paginator import Paginator
from rtchat.helpers import get_visible_chatrooms



@login_required
def chat_view(request, chatroom_name="public-chat"):
    """
    顯示聊天視圖
    """
    # 獲取指定的聊天室，並提前加載關聯的成員和消息作者
    chat_group = get_object_or_404(ChatGroup.objects.prefetch_related('members', 'chat_messages__author'), group_name=chatroom_name)

    # 驗證用戶是否有權訪問該聊天室
    if not chat_group.user_can_access(request.user):
        raise Http404("您無權訪問此聊天群組")

    # 如果是私人聊天室，找到聊天對象
    other_user = None
    if chat_group.is_private:
        other_user = chat_group.members.exclude(id=request.user.id).first()

    # 標記未讀消息為已讀
    chat_group.chat_messages.filter(is_unread=True).exclude(author=request.user).update(is_unread=False)

    # 分頁加載聊天消息
    all_messages = chat_group.chat_messages.all().order_by('-created')  # 按創建時間降序排序
    paginator = Paginator(all_messages, 30)  # 每頁顯示 30 條消息
    page_number = request.GET.get('page', 1)  # 從 GET 參數中獲取頁碼，默認為第 1 頁
    chat_messages = paginator.get_page(page_number)

    # 如果是 HTMX 發出的 POST 請求，處理消息創建
    if request.htmx and request.method == "POST":
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            # 返回部分渲染的消息模板
            return render(request, "rtchat/partials/chat_message_p.html", {"message": message, "user": request.user})

    # 渲染聊天模板
    form = ChatmessageCreateForm()
    return render(request, "rtchat/chat.html", {
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
        "chat_group": chat_group,
    })


@login_required
def get_or_create_chatroom(request, username):
    """
    獲取或創建與指定用戶的私人聊天室
    """
    username = unquote(username)
    other_user = get_object_or_404(User, username=username)

    if request.user == other_user:
        raise Http404("無法與自己建立聊天室")

    # 獲取或創建與指定用戶的唯一聊天室
    chatroom = ChatGroup.get_or_create_group_for_users([request.user, other_user])

    # 跳轉到聊天室頁面
    return redirect("rtchat:chatroom", chatroom.group_name)



@login_required
def redirect_to_first_chatroom(request):
    """
    將用戶重定向到他們的第一個聊天室，若無則返回首頁
    """
    # 獲取當前用戶參與的第一個聊天室
    chatroom = request.user.chat_groups.filter(members=request.user).first()
    if chatroom:
        return redirect('rtchat:chatroom', chatroom.group_name)

    # 如果用戶沒有任何聊天室，顯示提示消息並跳轉到首頁
    messages.info(request, "您尚未加入任何聊天室")
    return redirect('pages:home')




@login_required
def unread_notifications_count_chat(request):
    """
    返回當前用戶所有聊天室未讀消息的總數和紅點狀態
    """
    unread_count = sum(
        chatroom.chat_messages.filter(is_unread=True).exclude(author=request.user).count()
        for chatroom in request.user.chat_groups.all()
    )
    return JsonResponse({
        "unread_count": unread_count,
        "show_red_dot": unread_count > 0,  # 如果有未讀消息，顯示紅點
    })





