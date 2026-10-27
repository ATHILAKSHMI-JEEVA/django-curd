from django.contrib import admin
from .models import  Role,UserRole,File,TeamMember

admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(File)
admin.site.register(TeamMember)