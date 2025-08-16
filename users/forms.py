# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Profile

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """
    A form for creating new users, with validation and automatic Bootstrap styling.
    """
    # Define fields with their specific widgets and help text
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'e.g., yourname@example.com'}),
        help_text='Required. A valid email address.'
    )
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., +2349012345678'}),
        help_text='Required. Enter a valid phone number.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # A clear, explicit list of fields to be displayed, including password fields from the parent form.
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        """
        Add the Bootstrap 'form-control' class to each field's widget.
        """
        super().__init__(*args, **kwargs)
        # This loop applies styling to all fields, including the username and password fields
        # inherited from UserCreationForm.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'

    def clean_email(self):
        """Ensure the email address is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_phone_number(self):
        """Ensure the phone number is unique."""
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("An account with this phone number already exists.")
        return phone_number

    def save(self, commit=True):
        """
        Save the user and add them to the 'reader' group.
        """
        user = super().save(commit=False)
        # The UserCreationForm handles username and passwords.
        # We just need to ensure our custom fields are saved.
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
            # Add every new user to the 'reader' group by default
            reader_group, created = Group.objects.get_or_create(name='reader')
            user.groups.add(reader_group)
        return user
    
class UserUpdateForm(forms.ModelForm):
    """
    A form for updating user information, excluding password fields.
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        """
        Add the Bootstrap 'form-control' class to each field's widget.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control form-control-lg'

class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating user profile information.
    """
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'           