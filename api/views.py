from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer


class TaskPagination(PageNumberPagination):
    """Custom pagination class for Task viewset."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task model providing CRUD operations.
    
    Supports filtering by:
    - completada
    - prioridad
    - titulo
    - fecha_vencimiento_min
    - fecha_vencimiento_max
    
    Supports ordering by:
    - titulo
    - prioridad
    - fecha_vencimiento
    - fecha_creacion
    
    Supports search in titulo and descripcion.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['completada', 'prioridad', 'titulo']
    ordering_fields = ['titulo', 'prioridad', 'fecha_vencimiento', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    
    def get_queryset(self):
        """
        Override to add custom filtering for fecha_vencimiento range.
        """
        queryset = super().get_queryset()
        
        # Filter by fecha_vencimiento_min
        fecha_vencimiento_min = self.request.query_params.get('fecha_vencimiento_min')
        if fecha_vencimiento_min:
            queryset = queryset.filter(fecha_vencimiento__gte=fecha_vencimiento_min)
        
        # Filter by fecha_vencimiento_max
        fecha_vencimiento_max = self.request.query_params.get('fecha_vencimiento_max')
        if fecha_vencimiento_max:
            queryset = queryset.filter(fecha_vencimiento__lte=fecha_vencimiento_max)
        
        return queryset

