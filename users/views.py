from django.shortcuts import render
from .forms import UserRegistrationForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

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
    return render(request, 'users/login.html')