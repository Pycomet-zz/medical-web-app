from django.contrib import admin
from .models import RegularProfile, PractitionerProfile

admin.site.register(RegularProfile)
admin.site.register(PractitionerProfile)