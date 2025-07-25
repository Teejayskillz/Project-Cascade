from django.shortcuts import render
from .forms import UserRegistrationForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate , logout
from django.shortcuts import redirect


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