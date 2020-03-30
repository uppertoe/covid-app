from django.contrib import admin
from .models import Availability, Specialty, State, UserProfile, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Availability)
admin.site.register(Specialty)
admin.site.register(State)