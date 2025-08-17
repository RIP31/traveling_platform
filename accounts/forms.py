from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=150, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email Address")
    phone = forms.CharField(max_length=15, required=True, label="Phone Number")
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, label="Select Role")
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'role', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Use email as username for simplicity
        user.username = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
