from rest_framework import serializers
from .models import Task
from datetime import date


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion']
    
    def validate_titulo(self, value):
        """Validate that titulo is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío.")
        return value
    
    def validate_prioridad(self, value):
        """Validate that prioridad is one of the valid choices."""
        valid_choices = ['baja', 'media', 'alta']
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"La prioridad debe ser una de: {', '.join(valid_choices)}"
            )
        return value
    
    def validate_fecha_vencimiento(self, value):
        """Validate that fecha_vencimiento is not in the past (optional)."""
        if value and value < date.today():
            raise serializers.ValidationError(
                "La fecha de vencimiento no puede ser anterior a hoy."
            )
        return value
