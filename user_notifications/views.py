# notifications/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse

from notifications.models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
    
    def get(self, request, *args, **kwargs):
        request.user.notifications.all().mark_all_as_read()
        return super().get(request, *args, **kwargs)
    


@login_required
def get_unread_notifications(request):
    notifications = request.user.notifications.unread()[:5]  
    data = [
        {
            "id": n.id,
            "actor": str(n.actor),
            "verb": n.verb,
            "timestamp": n.timestamp.strftime("%H:%M"),
            "actor_url": reverse('users:user_profile', kwargs={'username': n.actor.username}) # Add this line
        }
        for n in notifications
    ]
    return JsonResponse({"count": notifications.count(), "notifications": data})