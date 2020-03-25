from django.contrib import admin
from .models import Availability, Specialty, State, Clinician

# Register your models here.
admin.site.register(Availability)
admin.site.register(Specialty)
admin.site.register(State)
admin.site.register(Clinician)