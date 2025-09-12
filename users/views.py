# users/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm , AuthorApplicationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .models import CustomUser, Profile, AuthorApplication, Subscribe
from django.contrib import messages



def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user; the signal will automatically create the profile.
            user = form.save()
            messages.success(request, f"Account created for {form.cleaned_data.get('username')}. You can now log in.")
            return render(request, 'users/success.html') # Render the success page
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

# Updated permission strings
@login_required(login_url='login_user')
@permission_required('users.view_customuser', login_url='login_user')
def user_list_view(request):
    users = CustomUser.objects.all().order_by('username')
    context = {
        'users': users,
        'page_title': 'Manage Users',
        'can_add_user': request.user.has_perm('users.add_customuser'),
        'can_change_user': request.user.has_perm('users.change_customuser'),
        'can_delete_user': request.user.has_perm('users.delete_customuser'),
    }
    return render(request, 'users/user_list.html', context)

# Updated permission strings
@login_required(login_url='login_user')
@permission_required('users.add_customuser', login_url='login_user')
def user_add_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user, the signal will automatically create the profile.
            user = form.save()
            messages.success(request, f"User '{form.cleaned_data['username']}' added successfully.")
            return redirect('users:user_list')
        else:
            messages.error(request, "Error adding user. Please correct the errors below.")
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
        'page_title': 'Add User',
    }
    return render(request, 'users/user_add.html', context)


# Updated permission strings and redirect name
@login_required(login_url='login_user')
@permission_required('users.change_customuser', login_url='login_user')
def user_toggle_active_view(request, user_id):
    user_toggle = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user_toggle.is_active = not user_toggle.is_active
        user_toggle.save()
        status_message = "activated" if user_toggle.is_active else "deactivated"
        messages.success(request, f"User '{user_toggle.username}' has been {status_message}.")

        if not user_toggle.is_active and request.user == user_toggle:
            logout(request)
            messages.info(request, "Your account has been deactivated. You have been logged out.")
            return redirect('login_user')

        return redirect('users:user_list')
    else: 
        context = {
            'user_obj': user_toggle,
            'action': 'activate' if not user_toggle.is_active else 'deactivate',
            'page_title': f"{'Activate' if not user_toggle.is_active else 'Deactivate'} User",
            'confirm_message': f"Are you sure you want to {'activate' if not user_toggle.is_active else 'deactivate'} user '{user_toggle.username}'?",
            'confirm_button_text': f"{'Activate' if not user_toggle.is_active else 'Deactivate'} User",
            'back_url': 'users:user_list'
        }
        return render(request, 'users/user_confirm_action.html', context)

# Updated permission strings and redirect name
@login_required(login_url='login_user')
@permission_required('users.delete_customuser', raise_exception=True)    
def user_delete_view(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, pk=user_id)
    if request.user == user_to_delete:
        messages.error(request, "You cannot delete your own account through this panel.")
        return redirect('users:user_list')
    
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User '{username}' has been successfully deleted")
        return redirect('users:user_list')
    context = {
        'user_obj': user_to_delete, # Corrected variable name
        'action': 'delete',
        'page_title': 'Delete User',
        'confirm_message': f"Are you sure you want to permanently delete user '{user_to_delete.username}'? This action cannot be undone.",
        'confirm_button_text': 'Delete User',
        'back_url': 'users:user_list'
    }
    return render(request, 'users/user_confirm_action.html', context)


def user_profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    # Default to False
    is_subscribed = False

    # Only check if the user is not viewing their own profile
    if request.user.is_authenticated and request.user != profile_user:
        is_subscribed = Subscribe.objects.filter(
            subscriber=request.user, subscribed_to=profile_user
        ).exists()
     # Check if the user is an author based on their role
    is_author = (profile_user.role == 'author')

    if request.user.is_authenticated and request.user != profile_user:
        # Check for subscription only if the profile user is an author
        if is_author:
            is_subscribed = Subscribe.objects.filter(
                subscriber=request.user, subscribed_to=profile_user
            ).exists()

    context = {
        'profile_user': profile_user,
        'page_title': f"{profile_user.username}'s Profile",
        'is_subscribed': is_subscribed, # ✅ changed from is_following to is_subscribed
        'is_author': is_author,  # ✅ new context variable
    }
    return render(request, 'users/user_profile.html', context)

@login_required(login_url='login_user')
def edit_profile_view(request):
    if request.method == 'POST':    
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # Check for profile existence before creating the form
        if hasattr(request.user, 'profile'):
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        else:
            profile_form = ProfileUpdateForm(request.POST, request.FILES) # No instance to update

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('users:user_profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        # Check for profile existence before creating the form
        if hasattr(request.user, 'profile'):
            profile_form = ProfileUpdateForm(instance=request.user.profile)
        else:
            profile_form = ProfileUpdateForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'page_title': "Edit Profile",
    }    
    return render(request, 'users/edit_profile.html', context)

@login_required(login_url='login_user')
def apply_for_author_view(request):
    # Check if the user already has a pending or approved application
    if AuthorApplication.objects.filter(user=request.user, status__in=['pending', 'approved']).exists():
        messages.warning(request, "You already have a pending or approved application.")
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        # Correctly instantiate the form with request.POST and request.FILES
        form = AuthorApplicationForm(request.POST, request.FILES) 
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('dashboard:dashboard')
    else:
        form = AuthorApplicationForm()

    context = {
        'form': form,
        'page_title': 'Apply for Author Role',
    }
    return render(request, 'users/apply_for_author.html', context)

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def manage_author_applications(request):
    """
    Displays all pending author applications.
    """
    applications = AuthorApplication.objects.filter(status='pending').order_by('-id')
    
    context = {
        'applications': applications
    }
    return render(request, 'users/manage_applications.html', context)


@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def approve_or_reject_application(request, app_id, action): 
    """
    Approves or rejects a specific author application.
    """
    if request.method == 'POST':
        application = get_object_or_404(AuthorApplication, id=app_id)  

        if action == 'approve':
            # Update the application status
            application.status = 'approved'
            application.save()
            
            # Get the user and update their role
            user_to_promote = application.user
            user_to_promote.role = 'author' 
            user_to_promote.save()
            
            messages.success(request, "Application approved and user's role set to Author!")
        elif action == 'reject':
            application.status = 'rejected'
            application.save()
            messages.info(request, "Application rejected.")
        
    return redirect('users:manage_applications')
@login_required
def user_subscribe_view(request, username):
    user_to_subscribe = get_object_or_404(CustomUser, username=username)

    if user_to_subscribe.role != 'author':
        messages.error(request, "You can only subscribe to authors.")
        return redirect('users:user_profile', username=username)


    if request.user == user_to_subscribe:
        messages.error(request, "You cannot subscribe to yourself.")
        return redirect('users:user_profile', username=username)

    subscription, created = Subscribe.objects.get_or_create(
        subscriber=request.user, subscribed_to=user_to_subscribe
    )
    if created:
        messages.success(request, f"You have successfully subscribed to {user_to_subscribe.username}.")
    else:
        messages.info(request, f"You are already subscribed to {user_to_subscribe.username}.")

    return redirect('users:user_profile', username=username)

@login_required
def user_unsubscribe_view(request, username):
    """
    Handles unsubscribing a user from another user.
    """
    user_to_unsubscribe = get_object_or_404(CustomUser, username=username)

    if request.user == user_to_unsubscribe:
        messages.error(request, "You cannot unsubscribe from yourself.")
        return redirect('users:user_profile', username=username)

    # Use the new model 'Subscribe' and its new field names
    deleted, _ = Subscribe.objects.filter(
        subscriber=request.user, 
        subscribed_to=user_to_unsubscribe
    ).delete()

    if deleted:
        messages.success(request, f"You have unsubscribed from {user_to_unsubscribe.username}.")
    else:
        messages.info(request, f"You are not subscribed to {user_to_unsubscribe.username}.")

    return redirect('users:user_profile', username=username)