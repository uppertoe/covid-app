from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import UserLogin, UserProfile

class SignUpForm(UserCreationForm):
    class Meta:
        model = UserLogin
        fields = ('email', 'password1', 'password2',)

class UserForm(ModelForm):
    class Meta:
        model = UserLogin
        fields = ['first_name', 'last_name',]

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobile', 'specialty', 'state',]