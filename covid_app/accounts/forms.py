from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',]

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobile', 'specialty',]