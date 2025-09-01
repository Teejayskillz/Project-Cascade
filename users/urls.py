from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    register_user, login_user, logout_user, user_list_view, user_add_view, 
    user_delete_view, user_toggle_active_view, user_profile_view, 
    edit_profile_view, apply_for_author_view, manage_author_applications, 
    approve_or_reject_application, user_subscribe_view, user_unsubscribe_view
)

app_name = 'users'

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('users/', user_list_view, name='user_list'),
    path('profile/<str:username>', user_profile_view, name='user_profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('users/add/', user_add_view, name='user_add'),
    path('users/<int:user_id>/toggle-active/', user_toggle_active_view, name='user_toggle_active'),
    path('users/<int:user_id>/delete/', user_delete_view, name='user_delete'),
    path('manage-applications/', manage_author_applications, name='manage_applications'),
    path('apply-for-author/', apply_for_author_view, name='apply_for_author'),
    path('applications/<int:app_id>/<str:action>/', approve_or_reject_application, name='approve_or_reject'),
    path("subscribe/<str:username>/", user_subscribe_view, name="user_subscribe"),
    path("unsubscribe/<str:username>/", user_unsubscribe_view, name="user_unsubscribe"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)