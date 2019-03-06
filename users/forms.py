from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RegularProfile, PractitionerProfile
from django.db import transaction

class UserRegisterForm(UserCreationForm):
    """Adding email field to the user register form"""

    email = forms.EmailField(help_text="Please input a valid email.")
    
    class Meta:
        """Gives a nested name space for configuration"""

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        """Saving each user"""

        user = super().save(commit=False)
        user.is_regular = True
        user.save()
        return user

class PractitionerRegisterForm(UserCreationForm):
    """Adding email field to the practitioner register form"""

    email = forms.EmailField(help_text="Please input a valid email.")
    
    class Meta:
        """Gives a nested name space for configuration"""

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        """Saving each user"""

        user = super().save(commit=False)
        user.is_practitioner = True
        user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    """Updating User info"""

    email = forms.EmailField(help_text="Please input a valid email.")

    class Meta:
        """Gives a nested name space for configuration"""

        model = User
        fields = ['username', 'email']

class RegularProfileUpdateForm(forms.ModelForm):
    """Updating Regular User Profile info"""

    class Meta:
        """Gives a nested name space for configuration"""

        model = RegularProfile
        fields = ['image']

class PractitionerProfileUpdateForm(forms.ModelForm):
    """Updating Practitioner User Profile info"""

    class Meta:
        """Gives a nested name space for configuration"""

        model = PractitionerProfile
        fields = ['image']

class MedicalForm(forms.ModelForm):
    """Updating Medical Information"""

    class Meta:
        """Gives a nested name space for configuration"""

        model = RegularProfile
        fields = ['malaria', 'typhoid', 'cholera', 'fever', 'small_pox', 'apollo', 'measles']

