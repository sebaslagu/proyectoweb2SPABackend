from django.db import models

# Create your models here.


class Task(models.Model):
    """Task model for managing tasks with priority and due dates."""
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=500, blank=True)
    completada = models.BooleanField(default=False)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'task'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo

