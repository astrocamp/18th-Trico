from .models import Notification


def send_notification(actor, recipient, verb, description=None, target_service=None):
    """
    發送通知
    :param actor: 發送通知的用戶
    :param recipient: 接收通知的用戶
    :param verb: 動作描述 (例如 "點讚" 或 "評論")
    :param description: 通知的描述
    :param target_service: 通知關聯的服務
    """
    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        description=description,
        target_service=target_service,
    )
