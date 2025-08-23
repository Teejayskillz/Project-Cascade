# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from wallet.models import Wallet

@login_required(login_url='login_user') # Change to your login URL name
def dashboard_view(request):
    wallet = None

    try: 
        wallet = request.user.wallet
    except Wallet.DoesNotExist:    
        pass
        
    context = {
        'page_title': 'Your Dashboard',
        'wallet': wallet,
        # Corrected permission string to match your CustomUser model
        'can_view_user_list': request.user.has_perm('users.view_customuser'),
        # Check for staff or superuser status for displaying user counts
        'total_users': CustomUser.objects.count() if request.user.is_staff or request.user.is_superuser else None,
        'active_users': CustomUser.objects.filter(is_active=True).count() if request.user.is_staff or request.user.is_superuser else None,
    }

    return render(request, 'dashboard/dashboard.html', context)