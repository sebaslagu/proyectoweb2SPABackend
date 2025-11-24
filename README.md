# Django REST API - Task Management Backend

Backend API para gestión de tareas construido con Django REST Framework.

## 📋 Características

- ✅ API REST completa con operaciones CRUD
- 🔍 Filtrado avanzado por múltiples campos
- 📊 Ordenamiento flexible
- 📄 Paginación configurable
- 🔐 Panel de administración de Django
- ✨ Validaciones de datos
- 🧪 Suite completa de pruebas

## 🛠️ Tecnologías

- Python 3.12+
- Django 4.2
- Django REST Framework 3.14+
- django-filter 23.0+
- django-cors-headers 4.0+
- SQLite (Base de datos por defecto)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/sebaslagu/proyectoweb2SPABackend.git
cd proyectoweb2SPABackend
```

### 2. Crear y activar entorno virtual (Opcional pero recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Realizar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar datos de prueba (Opcional)

```bash
python manage.py load_initial_data
```

Este comando carga 5 tareas de ejemplo en la base de datos.

### 6. Crear superusuario (Opcional)

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tareas/` | Listar todas las tareas |
| POST | `/api/tareas/` | Crear una nueva tarea |
| GET | `/api/tareas/{id}/` | Obtener una tarea específica |
| PUT | `/api/tareas/{id}/` | Actualizar completamente una tarea |
| PATCH | `/api/tareas/{id}/` | Actualizar parcialmente una tarea |
| DELETE | `/api/tareas/{id}/` | Eliminar una tarea |

## 🔍 Filtros y Búsqueda

### Filtros disponibles

- **completada**: Filtrar por estado de completado (`true` o `false`)
- **prioridad**: Filtrar por prioridad (`baja`, `media`, `alta`)
- **titulo**: Filtrar por título exacto
- **fecha_vencimiento_min**: Filtrar tareas con fecha de vencimiento mayor o igual
- **fecha_vencimiento_max**: Filtrar tareas con fecha de vencimiento menor o igual

### Ejemplos de uso

```bash
# Tareas completadas
GET /api/tareas/?completada=true

# Tareas de alta prioridad
GET /api/tareas/?prioridad=alta

# Tareas por título
GET /api/tareas/?titulo=Comprar%20leche

# Tareas por rango de fechas
GET /api/tareas/?fecha_vencimiento_min=2025-01-01&fecha_vencimiento_max=2025-12-31

# Búsqueda en título y descripción
GET /api/tareas/?search=médico
```

## 📊 Ordenamiento

Puedes ordenar los resultados usando el parámetro `ordering`:

```bash
# Ordenar por fecha de vencimiento (ascendente)
GET /api/tareas/?ordering=fecha_vencimiento

# Ordenar por prioridad (descendente)
GET /api/tareas/?ordering=-prioridad

# Ordenar por fecha de creación
GET /api/tareas/?ordering=fecha_creacion

# Ordenar por título
GET /api/tareas/?ordering=titulo
```

## 📄 Paginación

Por defecto, la API devuelve 10 resultados por página.

```bash
# Primera página
GET /api/tareas/?page=1

# Especificar tamaño de página
GET /api/tareas/?page=1&page_size=5

# Segunda página con 20 resultados
GET /api/tareas/?page=2&page_size=20
```

## 📝 Ejemplos de Requests

### Crear una tarea

```bash
curl -X POST http://127.0.0.1:8000/api/tareas/ \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Nueva tarea",
    "descripcion": "Descripción de la tarea",
    "prioridad": "alta",
    "completada": false,
    "fecha_vencimiento": "2025-12-31"
  }'
```

### Listar tareas

```bash
curl http://127.0.0.1:8000/api/tareas/
```

### Obtener una tarea específica

```bash
curl http://127.0.0.1:8000/api/tareas/1/
```

### Actualizar una tarea (PATCH)

```bash
curl -X PATCH http://127.0.0.1:8000/api/tareas/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "completada": true
  }'
```

### Eliminar una tarea

```bash
curl -X DELETE http://127.0.0.1:8000/api/tareas/1/
```

## 🧪 Ejecutar Tests

Para ejecutar la suite completa de pruebas:

```bash
python manage.py test api
```

Para ejecutar con más verbosidad:

```bash
python manage.py test api --verbosity=2
```

Para ejecutar una prueba específica:

```bash
python manage.py test api.tests.TaskAPITest.test_create_task
```

### Cobertura de Tests

Los tests incluyen:
- ✅ Creación de tareas
- ✅ Listado de tareas
- ✅ Obtención de tarea individual
- ✅ Actualización completa (PUT)
- ✅ Actualización parcial (PATCH)
- ✅ Eliminación de tareas
- ✅ Filtros por completada, prioridad y título
- ✅ Filtros por rango de fechas
- ✅ Ordenamiento
- ✅ Paginación
- ✅ Validaciones de datos
- ✅ Manejo de errores 400 y 404
- ✅ Búsqueda de texto

## 🗂️ Estructura del Proyecto

```
proyectoweb2SPABackend/
├── api/
│   ├── migrations/
│   │   └── 0001_initial.py
│   ├── management/
│   │   └── commands/
│   │       └── load_initial_data.py
│   ├── __init__.py
│   ├── admin.py          # Configuración del admin
│   ├── apps.py
│   ├── models.py         # Modelo Task
│   ├── serializers.py    # TaskSerializer
│   ├── tests.py          # Tests completos
│   ├── urls.py           # URLs de la API
│   └── views.py          # TaskViewSet
├── backend/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py       # Configuración del proyecto
│   ├── urls.py           # URLs principales
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## 📋 Modelo de Datos

### Task

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | AutoField | ID único (automático) |
| titulo | CharField(150) | Título de la tarea (requerido) |
| descripcion | CharField(500) | Descripción de la tarea (opcional) |
| completada | BooleanField | Estado de completado (default: False) |
| prioridad | CharField(20) | Prioridad: baja, media, alta |
| fecha_vencimiento | DateField | Fecha de vencimiento (opcional) |
| fecha_creacion | DateTimeField | Fecha de creación (automático) |

## 🔐 Panel de Administración

Accede al panel de administración en `http://127.0.0.1:8000/admin/`

Características:
- Listado de tareas con campos clave
- Filtros por completada, prioridad y fecha
- Búsqueda por título y descripción
- Edición en línea

## 📊 Datos de Prueba

El comando `load_initial_data` carga las siguientes tareas:

1. **Comprar leche** 
2. **Llamar al médico**
3. **Enviar informe** 
4. **Leer 30 minutos** 
5. **Pagar servicios** 
