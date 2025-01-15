from django import template

register = template.Library()

@register.filter
def chatrooms_list(user):
    """過濾並返回用戶的聊天室列表"""
    chatrooms = user.chat_groups.distinct()
    processed_users = set()  # 已處理的用戶
    unique_chatrooms = []

    for chatroom in chatrooms:
        for member in chatroom.members.all():
            if member != user and member.username not in processed_users:
                processed_users.add(member.username)
                unique_chatrooms.append(chatroom)
                break
    return unique_chatrooms

@register.filter
def unread_count(chatroom, user):
    """計算聊天室中未讀消息的數量"""
    return chatroom.chat_messages.filter(is_unread=True).exclude(author=user).count()
