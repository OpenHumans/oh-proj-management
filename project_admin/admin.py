from django.contrib import admin
from .models import Project, ProjectGroup, ProjectMember, File, Note
# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectGroup)
admin.site.register(ProjectMember)
admin.site.register(File)
admin.site.register(Note)
