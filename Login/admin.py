from django.contrib import admin
from .models import ConfirmationCode

@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created_at')
    search_fields = ('email', 'code')
