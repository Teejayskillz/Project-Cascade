from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import userRegistration

@login_required(login_url='login')
def dashboard_view(request):
    # This context dictionary is where you add the permission check
    context = {
        'page_title': 'Your Dashboard',
        'can_view_user_list': request.user.has_perm('users.view_userregistration'),
        'total_users': userRegistration.objects.count() if request.user.is_staff or request.user.is_superuser else None,
        'active_users': userRegistration.objects.filter(is_active=True).count() if request.user.is_staff or request.user.is_superuser else None,
    }

    return render(request, 'dashboard/dashboard.html', context)