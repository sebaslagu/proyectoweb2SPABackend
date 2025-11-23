from django.core.management.base import BaseCommand
from api.models import Task
from datetime import date


class Command(BaseCommand):
    help = 'Load initial task data'

    def handle(self, *args, **kwargs):
        # Clear existing tasks
        Task.objects.all().delete()
        
        # Create sample tasks
        tasks_data = [
            {
                "titulo": "Comprar leche",
                "descripcion": "Leche y pan",
                "completada": False,
                "prioridad": "media",
                "fecha_vencimiento": date(2025, 12, 1)
            },
            {
                "titulo": "Llamar al médico",
                "descripcion": "Cita dental",
                "completada": False,
                "prioridad": "alta",
                "fecha_vencimiento": date(2025, 11, 28)
            },
            {
                "titulo": "Enviar informe",
                "descripcion": "",
                "completada": True,
                "prioridad": "alta",
                "fecha_vencimiento": date(2025, 10, 10)
            },
            {
                "titulo": "Leer 30 minutos",
                "descripcion": "Libro técnico",
                "completada": False,
                "prioridad": "baja",
                "fecha_vencimiento": None
            },
            {
                "titulo": "Pagar servicios",
                "descripcion": "Agua y luz",
                "completada": False,
                "prioridad": "media",
                "fecha_vencimiento": date(2025, 11, 30)
            }
        ]
        
        for task_data in tasks_data:
            Task.objects.create(**task_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(tasks_data)} tasks'))
