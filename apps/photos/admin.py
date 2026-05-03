from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_name', 'created_at']
    readonly_fields = ['image', 'watermarked', 'original_name', 'created_at']
