from django.contrib import admin
from .models import Organization, Branch

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_active", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("is_active",)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "code", "email", "is_active")
    search_fields = ("name", "code", "organization__name")
    list_filter = ("is_active", "organization")
