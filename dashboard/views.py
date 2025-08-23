# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import CustomUser, AuthorApplication # Import the AuthorApplication model
from wallet.models import Wallet

@login_required(login_url='login_user')
def dashboard_view(request):
    wallet = None
    author_application = None

    try:
        wallet = request.user.wallet
    except Wallet.DoesNotExist:
        pass

    # Check if the user is a regular user (not staff/superuser) and not an author
    if not request.user.is_staff and not request.user.is_superuser:
        try:
            # Attempt to fetch the user's author application
            author_application = request.user.author_application
        except AuthorApplication.DoesNotExist:
            pass # No application found, `author_application` remains None

    context = {
        'page_title': 'Your Dashboard',
        'wallet': wallet,
        'can_view_user_list': request.user.has_perm('users.view_customuser'),
        'total_users': CustomUser.objects.count() if request.user.is_staff or request.user.is_superuser else None,
        'active_users': CustomUser.objects.filter(is_active=True).count() if request.user.is_staff or request.user.is_superuser else None,
        'author_application': author_application, # Pass the application object to the template
    }

    return render(request, 'dashboard/dashboard.html', context)