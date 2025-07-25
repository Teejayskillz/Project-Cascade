# users/forms.py (assuming this is your forms.py)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Get your custom user model, which is 'users.UserRegistration' as per your settings
User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    # Additional fields
    phone_number = forms.CharField(max_length=15,
                                    required=True,
                                    widget=forms.TextInput(attrs={
                                        'placeholder': 'e.g +23490387222',
                                    }),
                                    help_text='Required. Enter a valid phone number.')
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'your email address'
                             }),
                             help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    # Corrected: 'Meta' with a capital 'M'
    class Meta(UserCreationForm.Meta):
        model = User # This correctly points to your custom UserRegistration model
        # Ensure all fields you want to be managed by the form are listed here,
        # including the default ones from UserCreationForm.Meta.fields if you want them.
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',) + UserCreationForm.Meta.fields
        # Or you can list them explicitly if you prefer:
        # fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'password2')
        # Note: 'password', 'password2' are typically handled by UserCreationForm directly,
        # but listing them ensures they are included if you modify the base fields.

        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            # 'password': 'Password', # No need for password1/2 in labels
            # 'password2': 'Confirm Password',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if an email already exists, excluding the current user's email if updating
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address already in use.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Check if a phone number already exists, excluding the current user's phone if updating
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already in use.")
        return phone_number

    def save(self, commit=True):
        # Call the parent save method, which handles username and password
        user = super().save(commit=False)
        # Set your custom fields
        user.email = self.cleaned_data['email'] # Ensure email is saved as a field on the user model too
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
        return user