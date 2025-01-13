from django import template

register = template.Library()

@register.filter
def first_chatroom(user):
    
    # 找第一個符合條件的 chatroom，若無則返回 None。

    for chatroom in user.chat_groups.all():
        if chatroom.is_private:
            for member in chatroom.members.all():
                if member != user:
                    return chatroom
    return None
