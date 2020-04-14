from django.contrib import admin
from .models import CalendarDay, Shift

# Register your models here.
admin.site.register(CalendarDay)
admin.site.register(Shift)