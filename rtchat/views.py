from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import ChatGroup
from .forms import ChatmessageCreateForm
from django.contrib.auth.models import User
from urllib.parse import unquote


@login_required
def chat_view(request):
    user_chatrooms = request.user.chat_groups.filter(members=request.user).distinct()
    context = {
        'chatrooms': user_chatrooms,
    }
    return render(request, 'chat_template.html', context)

@login_required
def chat_view(request, chatroom_name="public-chat"):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all().select_related("author")[:30]
    form = ChatmessageCreateForm()
    
    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404("您無法訪問此聊天群組")
        other_user = chat_group.members.exclude(id=request.user.id).first()
        if not other_user:
            raise Http404("聊天對象並不存在。")

    
    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                "message" : message,
                "user" : request.user,
            }
            return render(request, "rtchat/partials/chat_message_p.html", context)
    
    context = {
        "chat_messages" : chat_messages, 
        "form" : form,
        "other_user" : other_user,
        "chatroom_name" : chatroom_name,
        "chat_group" : chat_group
    }
    
    return render(request, "rtchat/chat.html", context)





@login_required
def get_or_create_chatroom(request, username):
    # 獲取聊天對象
    username = unquote(username)
    other_user = get_object_or_404(User, username=username)

    # 防止與自己創建聊天室
    if request.user == other_user:
        raise Http404("無法與自己建立聊天室")

    # 查找是否已有私人聊天室
    chatroom = ChatGroup.objects.filter(
        members=request.user
    ).filter(members=other_user).first()

    # 如果不存在，創建新聊天室
    if not chatroom:
        chatroom = ChatGroup.objects.create()
        chatroom.members.add(request.user, other_user)

    # 跳轉到聊天室頁面
    return redirect('chatroom', chatroom.group_name)





@login_required
def redirect_to_first_chatroom(request):
    # 獲取當前用戶的第一個聊天室
    chatroom = request.user.chat_groups.filter(members=request.user).first()
    if chatroom:
        return redirect('chatroom', chatroom.group_name)
    return redirect('pages:home')  # 若無聊天室，跳轉到預設頁面
