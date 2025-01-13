from django import template

register = template.Library()

@register.filter
def chatrooms_list(user):
    # 返回與用戶相關的所有聊天室，並去重
    chatrooms = user.chat_groups.distinct()
    processed_users = set()  # 用來記錄已處理過的用戶
    unique_chatrooms = []

    for chatroom in chatrooms:
        for member in chatroom.members.all():
            if member != user and member.username not in processed_users:
                processed_users.add(member.username)  # 記錄處理過的用戶
                unique_chatrooms.append(chatroom)
                break  # 如果找到有效聊天室，就結束內層迴圈

    return unique_chatrooms
