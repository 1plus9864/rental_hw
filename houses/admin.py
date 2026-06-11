from django.contrib import admin
from .models import UserProfile
from .models import House
from .models import Favorite
from .models import Appointment

admin.site.register(Appointment)
admin.site.register(Favorite)
admin.site.register(UserProfile)
admin.site.register(House)