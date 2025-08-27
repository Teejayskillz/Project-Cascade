# user_notifications/urls.py

from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("notifications/json/", views.get_unread_notifications, name="unread_notifications_json"),
    path('unread-notifications/', views.get_unread_notifications, name='get_unread_notifications'),
]