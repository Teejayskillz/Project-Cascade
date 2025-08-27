# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_unread_notifications(request):
    notifications = request.user.notifications.unread()[:5]  
    data = [
        {
            "id": n.id,
            "actor": str(n.actor),
            "verb": n.verb,
            "timestamp": n.timestamp.strftime("%H:%M"),
        }
        for n in notifications
    ]
    return JsonResponse({"count": notifications.count(), "notifications": data})

