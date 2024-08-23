from django.contrib import admin
from .models import RoamingIn
from .models import RoamingOut

admin.site.register(RoamingIn)
admin.site.register(RoamingOut)
