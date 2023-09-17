from django.contrib import admin

# Register your models here.
from apps.Users.models import User

admin.site.register(User)