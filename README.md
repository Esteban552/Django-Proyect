# Tienda Online API

API REST desarrollada con Django y Django REST Framework para gestionar un catálogo y usuarios académicos. La documentación interactiva está en `/swagger/` y ReDoc en `/redoc/`.

## Requisitos

- Python 3.11 o superior
- Git

## Instalación local

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations users
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Por defecto usa SQLite para que se pueda ejecutar sin un servicio adicional; `db.sqlite3` está excluido de Git. Para usar el MySQL de la Unidad 1, configura `DB_ENGINE=mysql`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` como variables de entorno antes de migrar. `DJANGO_SECRET_KEY` se puede establecer para reemplazar la clave local de desarrollo.

## Endpoints principales

- `POST /api/v1/auth/token/` - obtiene access y refresh usando `email` y `password`.
- `POST /api/v1/auth/token/refresh/` - renueva el access token.
- `GET /api/v1/auth/me/` - consulta los datos propios; requiere `Authorization: Bearer <access>`.
- `/api/v1/users/` - CRUD administrativo; requiere un usuario staff.
- `/api/v1/products/` y `/api/v1/categories/` - catálogo existente.
- `/swagger/` - Swagger UI con título **Aula Digital API**.

El access token dura 30 minutos. El campo `student_id` (matrícula) aparece en admin, serializer y esquema OpenAPI. La contraseña es de solo escritura, se guarda con el hasher de Django y solo cambia al enviarla explícitamente en una actualización.
