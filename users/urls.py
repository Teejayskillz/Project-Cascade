from django.urls import path
from .views import register_user , login_user, logout_user , user_list_view, user_add_view, user_delete_view , user_toggle_active_view , user_profile_view , edit_profile_view

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('users/', user_list_view, name='user_list'),
    path('profile/', user_profile_view, name='user_profile'),  # Assuming this is for user profile view
    path('profile/edit/', edit_profile_view, name='edit_profile'),  # Assuming this is for editing user profile
    path('users/add/', user_add_view, name='user_add'),
    path('users/<int:user_id>/toggle-active/', user_toggle_active_view, name='user_toggle_active'),
    path('users/<int:user_id>/delete/', user_delete_view, name='user_delete'),
]