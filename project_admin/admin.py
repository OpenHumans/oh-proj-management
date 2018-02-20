from django.contrib import admin
from .models import Project
from .models import User


admin.site.register(Project)
admin.site.register(User)