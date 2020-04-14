from django.contrib import admin
from .models import Specialty, State, UserProfile, UserLogin
from avail_calendar.models import Shift
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Define an inline admin descriptor for UserProfile model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'

class ShiftInline(admin.StackedInline):
    model = Shift
    can_delete = False
    verbose_name_plural = 'shifts'

#Ensure that the email address is used as the username
@admin.register(UserLogin)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    #Link the UserProfile to the User admin view
    inlines = (UserProfileInline, ShiftInline)

# Register your models here.
admin.site.register(Specialty)
admin.site.register(State)