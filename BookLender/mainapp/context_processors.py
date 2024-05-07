from .models import UserNotification, UserProfile


def get_user_notifications(request):
    if request.user.is_authenticated:
        notifications = UserNotification.objects.filter(recipient__user=request.user, read=False)
        notification_count = notifications.count()
        print(notification_count, notifications)
        return {'notifications': notifications, 'notification_count': notification_count}
    return {}