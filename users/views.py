from django.shortcuts import render , get_object_or_404 , redirect
from .forms import UserRegistrationForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate , logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required , permission_required
from .models import userRegistration
from django.contrib import messages


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'users/success.html')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    # Placeholder for login logic
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or dashboard after login
            else:
                form.add_error(None, "Invalid username or password")
        return render(request, 'users/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_user(request):
    # Placeholder for logout logic

    logout(request)
    return redirect('home')  # Redirect to login page after logout    

@login_required(login_url='login')
@permission_required('users.view_userregistration', login_url='login')
def user_list_view(request):
    users = userRegistration.objects.all().order_by('username')
    context = {
        'users': users,
        'page_title': 'Manage Users',
        'can_add_user': request.user.has_perm('users.add_userregistration'),
        'can_change_user': request.user.has_perm('users.change_userregistration'),
        'can_delete_user': request.user.has_perm('users.delete_userregistration'),
    }
    return render(request, 'users/user_list.html', context)

@login_required(login_url='login')
@permission_required('users.view_userregistration', login_url='login')
def user_add_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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

@login_required(login_url='login') # Assuming 'login' is the URL name for your login page
@permission_required('users.change_userregistration', login_url='login') # Or raise_exception=True
def user_toggle_active_view(request, user_id):
    """
    Toggles the is_active status of a user.
    Handles both GET (confirmation) and POST (action) requests.
    """
    user_toggle = get_object_or_404(userRegistration, id=user_id)

    # --- POST Request Handling ---
    if request.method == 'POST':
        # Optional: Prevent a user from deactivating their own account via this view
        # if request.user == user_toggle:
        #     messages.error(request, "You cannot deactivate your own account directly from this page.")
        #     return redirect('user_list') # Redirect back to the user list or profile page

        user_toggle.is_active = not user_toggle.is_active # Toggle the status
        user_toggle.save()
        status_message = "activated" if user_toggle.is_active else "deactivated"
        messages.success(request, f"User '{user_toggle.username}' has been {status_message}.")

        # If the user being toggled is the currently logged-in user AND they are being deactivated, log them out
        if not user_toggle.is_active and request.user == user_toggle:
            logout(request)
            messages.info(request, "Your account has been deactivated. You have been logged out.")
            return redirect('login') # Redirect to login after self-deactivation

        return redirect('user_list') # Always redirect after a successful POST

    # --- GET Request Handling (Display Confirmation Page) ---
    else: 
        context = {
            'user_obj': user_toggle, # Corrected variable name
            'action': 'activate' if not user_toggle.is_active else 'deactivate', # Use lowercase for consistent action
            'page_title': f"{'Activate' if not user_toggle.is_active else 'Deactivate'} User",
            'confirm_message': f"Are you sure you want to {'activate' if not user_toggle.is_active else 'deactivate'} user '{user_toggle.username}'?",
            'confirm_button_text': f"{'Activate' if not user_toggle.is_active else 'Deactivate'} User",
            'back_url': 'user_list' # Assuming 'user_list' is the URL name for your user list
        }
        # Replace 'your_app_name/user_confirm_action.html' with the actual path to your template
        return render(request, 'users/user_confirm_action.html', context)
    
@login_required(login_url='login')
@permission_required('user.delete_userregistration' , raise_exception=True)    
def user_delete_view(request, user_id):
    user_to_delete = get_object_or_404(userRegistration, pk=user_id)
    if request.user == user_to_delete:
        messages.error(request, "you cannot delete your own account through this panel.")
        return redirect('user:user_list')
    
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"User '{username}' has been successfully deleted")
        return redirect('user_list')
    context = {
        'use_obj': user_to_delete,
        'action': 'delete',
        'page_title': 'Delete User',
        'confirm_message': f"Are you sure you want to permanently delete user '{user_to_delete.username}'? This action cannot be undone.",
        'confirm_button_text': 'Delete User',
        'back_url': 'user_list'
    }
    return render(request, 'users/user_confirm_action.html', context)





    