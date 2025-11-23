from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model."""
    list_display = ['titulo', 'prioridad', 'completada', 'fecha_vencimiento', 'fecha_creacion']
    list_filter = ['completada', 'prioridad', 'fecha_vencimiento', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']

