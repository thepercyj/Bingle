from django.contrib.auth.decorators import login_required

from .models import UserNotification, UserProfile


def get_user_notifications(request):
    """
    Get all unread notifications for the current user

    :param request: HttpRequest
    """
    if request.user.is_authenticated:
        notifications = UserNotification.objects.filter(recipient__user=request.user, read=False)
        notification_count = notifications.count()
        print(notification_count, notifications)
        return {'notifications': notifications, 'notification_count': notification_count}
    return {}


def get_profile_pic(request):
    """
    Get the profile picture for the current user

    :param request: HttpRequest
    """
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        print(profile.profile_pic.url)
        if profile.profile_pic.url != "/media/b''":
            return {'profile_pic': profile.profile_pic}
    return {}
