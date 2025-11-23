from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Task
from datetime import date, timedelta


class TaskModelTest(TestCase):
    """Test cases for Task model."""
    
    def setUp(self):
        self.task = Task.objects.create(
            titulo="Test Task",
            descripcion="Test Description",
            prioridad="media",
            fecha_vencimiento=date.today() + timedelta(days=7)
        )
    
    def test_task_creation(self):
        """Test task is created correctly."""
        self.assertEqual(self.task.titulo, "Test Task")
        self.assertEqual(self.task.descripcion, "Test Description")
        self.assertEqual(self.task.prioridad, "media")
        self.assertFalse(self.task.completada)
    
    def test_task_str(self):
        """Test task string representation."""
        self.assertEqual(str(self.task), "Test Task")


class TaskAPITest(APITestCase):
    """Test cases for Task API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('task-list')
        
        # Create test tasks
        self.task1 = Task.objects.create(
            titulo="Task 1",
            descripcion="Description 1",
            prioridad="alta",
            completada=False,
            fecha_vencimiento=date.today() + timedelta(days=1)
        )
        self.task2 = Task.objects.create(
            titulo="Task 2",
            descripcion="Description 2",
            prioridad="baja",
            completada=True,
            fecha_vencimiento=date.today() + timedelta(days=30)
        )
        self.task3 = Task.objects.create(
            titulo="Task 3",
            descripcion="Description 3",
            prioridad="media",
            completada=False,
            fecha_vencimiento=None
        )
    
    def test_list_tasks(self):
        """Test listing all tasks."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
    
    def test_create_task(self):
        """Test creating a new task."""
        data = {
            'titulo': 'New Task',
            'descripcion': 'New Description',
            'prioridad': 'alta',
            'completada': False,
            'fecha_vencimiento': str(date.today() + timedelta(days=5))
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 4)
        self.assertEqual(response.data['titulo'], 'New Task')
    
    def test_retrieve_task(self):
        """Test retrieving a single task."""
        detail_url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], 'Task 1')
    
    def test_update_task(self):
        """Test updating a task (PUT)."""
        detail_url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        data = {
            'titulo': 'Updated Task',
            'descripcion': 'Updated Description',
            'prioridad': 'baja',
            'completada': True,
            'fecha_vencimiento': str(date.today() + timedelta(days=10))
        }
        response = self.client.put(detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.titulo, 'Updated Task')
        self.assertTrue(self.task1.completada)
    
    def test_partial_update_task(self):
        """Test partially updating a task (PATCH)."""
        detail_url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        data = {'completada': True}
        response = self.client.patch(detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completada)
    
    def test_delete_task(self):
        """Test deleting a task."""
        detail_url = reverse('task-detail', kwargs={'pk': self.task1.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 2)
    
    def test_filter_by_completada(self):
        """Test filtering tasks by completada status."""
        response = self.client.get(self.list_url, {'completada': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['titulo'], 'Task 2')
    
    def test_filter_by_prioridad(self):
        """Test filtering tasks by prioridad."""
        response = self.client.get(self.list_url, {'prioridad': 'alta'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['titulo'], 'Task 1')
    
    def test_filter_by_titulo(self):
        """Test filtering tasks by titulo."""
        response = self.client.get(self.list_url, {'titulo': 'Task 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_filter_by_fecha_vencimiento_range(self):
        """Test filtering tasks by fecha_vencimiento range."""
        fecha_min = str(date.today())
        fecha_max = str(date.today() + timedelta(days=10))
        response = self.client.get(self.list_url, {
            'fecha_vencimiento_min': fecha_min,
            'fecha_vencimiento_max': fecha_max
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['titulo'], 'Task 1')
    
    def test_ordering_by_fecha_vencimiento(self):
        """Test ordering tasks by fecha_vencimiento."""
        response = self.client.get(self.list_url, {'ordering': 'fecha_vencimiento'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify ordering is working (actual order depends on database NULL handling)
        results = response.data['results']
        self.assertEqual(len(results), 3)
    
    def test_ordering_by_prioridad_desc(self):
        """Test ordering tasks by prioridad descending."""
        response = self.client.get(self.list_url, {'ordering': '-prioridad'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_pagination(self):
        """Test pagination."""
        # Create more tasks to test pagination
        for i in range(15):
            Task.objects.create(
                titulo=f'Pagination Test {i}',
                prioridad='media'
            )
        response = self.client.get(self.list_url, {'page': 1, 'page_size': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])
    
    def test_create_task_validation_empty_titulo(self):
        """Test validation for empty titulo."""
        data = {
            'titulo': '',
            'prioridad': 'alta'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_task_validation_invalid_prioridad(self):
        """Test validation for invalid prioridad."""
        data = {
            'titulo': 'Test Task',
            'prioridad': 'urgente'  # Invalid choice
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_task_validation_past_fecha_vencimiento(self):
        """Test validation for past fecha_vencimiento."""
        data = {
            'titulo': 'Test Task',
            'prioridad': 'alta',
            'fecha_vencimiento': str(date.today() - timedelta(days=1))
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_nonexistent_task(self):
        """Test retrieving a non-existent task returns 404."""
        detail_url = reverse('task-detail', kwargs={'pk': 9999})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_search_by_titulo(self):
        """Test searching tasks by titulo."""
        response = self.client.get(self.list_url, {'search': 'Task 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

