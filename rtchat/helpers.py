# rtchat/helpers.py
from .models import ChatGroup

def get_visible_chatrooms(user):
    """
    返回與用戶相關的所有聊天室，確保唯一且為可見聊天室
    """
    chatrooms = user.chat_groups.distinct()
    processed_users = set()
    unique_chatrooms = []

    for chatroom in chatrooms:
        for member in chatroom.members.all():
            if member != user and member.username not in processed_users:
                processed_users.add(member.username)
                unique_chatrooms.append(chatroom)
                break  # 找到唯一聊天室後結束內層迴圈

    return unique_chatrooms
