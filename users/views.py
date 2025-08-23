# users/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import CustomUser, Profile # Import CustomUser and Profile
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
            return redirect('user_list')
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

        return redirect('user_list')
    else: 
        context = {
            'user_obj': user_toggle,
            'action': 'activate' if not user_toggle.is_active else 'deactivate',
            'page_title': f"{'Activate' if not user_toggle.is_active else 'Deactivate'} User",
            'confirm_message': f"Are you sure you want to {'activate' if not user_toggle.is_active else 'deactivate'} user '{user_toggle.username}'?",
            'confirm_button_text': f"{'Activate' if not user_toggle.is_active else 'Deactivate'} User",
            'back_url': 'user_list'
        }
        return render(request, 'users/user_confirm_action.html', context)

# Updated permission strings and redirect name
@login_required(login_url='login_user')
@permission_required('users.delete_customuser', raise_exception=True)    
def user_delete_view(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, pk=user_id)
    if request.user == user_to_delete:
        messages.error(request, "You cannot delete your own account through this panel.")
        return redirect('user_list')
    
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User '{username}' has been successfully deleted")
        return redirect('user_list')
    context = {
        'user_obj': user_to_delete, # Corrected variable name
        'action': 'delete',
        'page_title': 'Delete User',
        'confirm_message': f"Are you sure you want to permanently delete user '{user_to_delete.username}'? This action cannot be undone.",
        'confirm_button_text': 'Delete User',
        'back_url': 'user_list'
    }
    return render(request, 'users/user_confirm_action.html', context)

@login_required(login_url='login_user')
def user_profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username) 
    context = {
        'profile_user': profile_user,
        'page_title': f"{profile_user.username}'s Profile",
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
            return redirect('user_profile', username=request.user.username)
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