from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# admin.site.register(Admin, UserAdmin)
# admin.site.register(Developer)
# admin.site.register(Project)

@admin.register(Admin)
class UserAdmin(admin.ModelAdmin):
    fields = ( "email", "password", "username", "designation", "experties", "is_superuser", "is_staff", "profile_pic", "phone_number","user_permissions",)
    list_display = ("username", "email", "is_staff", "designation")
    list_filter =  ("is_staff" ,"designation", "created_at","updated_at", "experties")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "assign_to", "status")
    list_filter =  ("status" ,"assign_to", "created_at","updated_at")

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "assign_to", "status")
    list_filter =  ("status" ,"assign_to", "created_at","updated_at")

