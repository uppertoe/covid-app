from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserProfileForm, UserForm
from .models import UserProfile, User

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('/content/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def user_profile_view(request):
    current_user = request.user
    current_user_profile = request.user.userprofile
    if request.method == 'POST':
        #Combines forms relating to the 'user' and 'userprofile' models
        user_form = UserForm(request.POST, instance = current_user)
        profile_form = UserProfileForm(request.POST, instance = current_user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form_instance = user_form.save()
            profile_form_instance = profile_form.save(commit = False)
            profile_form_instance.user = user_form_instance
            profile_form_instance.save()
            return redirect('/content/')
    context = {
        'user_form' : UserForm(instance = current_user),
        'profile_form': UserProfileForm(instance = current_user_profile),
    }
    return render(request, 'accounts/user_profile.html', context)