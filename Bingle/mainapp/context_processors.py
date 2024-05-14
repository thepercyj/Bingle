from django.contrib.auth.decorators import login_required

from .models import UserNotification, UserProfile


def get_user_notifications(request):
    """
    Get all unread notifications for the current user

    :param request: HttpRequest
    """
    if request.user.is_authenticated:
        notifications = UserNotification.objects.filter(recipient__user=request.user)
        read_notifications = notifications.filter(read=True)  # get the read notifications
        unread_notifications = notifications.filter(read=False)  # get the unread notifications
        unread_notification_count = notifications.count()  # get the count of unread notifications
        read_notification_count = read_notifications.count()

        notifications = reversed(notifications)
        read_notifications = reversed(read_notifications)

        return {'notifications':notifications, 'unread_notifications': unread_notifications, 'unread_notification_count': unread_notification_count,
                'read_notifications': read_notifications, read_notification_count: 'read_notification_count'}
    return {}


def get_profile_pic(request):
    """
    Get the profile picture for the current user

    :param request: HttpRequest
    """
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if profile.profile_pic:
            if profile.profile_pic.url != "/media/b''":
                return {'profile_pic': profile.profile_pic}
        else:
            return {}
    return {}
