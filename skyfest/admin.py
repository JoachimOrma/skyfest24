from django.contrib import admin
from .models import Attendee

# Register your models here.
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'parent_phone', 'qr_code', 'created_at']
    search_fields = ['first_name', 'last_name']