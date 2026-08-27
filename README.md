
---

```markdown
# 🚀 API de Gestión de Grupos y Formación

API RESTful desarrollada con **FastAPI**, **SQLAlchemy ORM** y **Pydantic** para la gestión integral de grupos de formación, estudiantes, instructores, entregas de trabajos, calificaciones, asistencias y notificaciones.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI
* **ORM:** SQLAlchemy
* **Validación de Datos:** Pydantic v2
* **Autenticación:** OAuth2 con JWT (JSON Web Tokens)
* **Seguridad:** Passlib (Bcrypt)
* **Base de Datos:** PostgreSQL / SQLite (según entorno)

---

## 📁 Estructura del Proyecto

```text
api_gestion_grupos/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── auth.py
│   ├── models/
│   │   ├── usuario.py
│   │   ├── estudiante.py
│   │   ├── instructor.py
│   │   ├── grupo.py
│   │   ├── trabajo.py
│   │   ├── entrega.py
│   │   ├── calificacion.py
│   │   ├── asistencia.py
│   │   └── notificacion.py
│   ├── schemas/
│   │   ├── usuario.py
│   │   ├── estudiante.py
│   │   ├── instructor.py
│   │   ├── grupo.py
│   │   ├── trabajo.py
│   │   ├── entrega.py
│   │   ├── calificacion.py
│   │   ├── asistencia.py
│   │   └── notificacion.py
│   └── routers/
│       ├── auth.py
│       ├── usuarios.py
│       ├── estudiantes.py
│       ├── instructores.py
│       ├── grupos.py
│       ├── trabajos.py
│       ├── entregas.py
│       ├── calificaciones.py
│       ├── asistencias.py
│       └── notificaciones.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

```

---

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd api_gestion_grupos

```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

```

### 4. Configurar variables de entorno (`.env`)

Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
DATABASE_URL=sqlite:///./sql_app.db
SECRET_KEY=tu_clave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

```

### 5. Ejecutar la aplicación

```bash
uvicorn app.main:app --reload

```

La aplicación estará disponible en `http://127.0.0.1:8000`.

---

## 📖 Documentación Interactiva (Swagger / ReDoc)

Una vez iniciada la aplicación, puedes acceder a:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Tabla Completa de Endpoints Implementados (44 Total)

| # | Módulo | Método | Ruta / Endpoint | Descripción | Autenticación / Rol |
| --- | --- | --- | --- | --- | --- |
| 1 | **Auth** | `POST` | `/auth/login` | Iniciar sesión y obtener token JWT | Público |
| 2 | **Auth** | `GET` | `/auth/me` | Obtener información del usuario autenticado | Requiere Token |
| 3 | **Usuarios** | `POST` | `/usuarios/` | Crear un nuevo usuario | Requiere Admin |
| 4 | **Usuarios** | `GET` | `/usuarios/` | Listar todos los usuarios | Requiere Admin |
| 5 | **Usuarios** | `GET` | `/usuarios/{id}` | Obtener un usuario por ID | Requiere Admin |
| 6 | **Usuarios** | `PUT` | `/usuarios/{id}` | Actualizar datos de un usuario | Requiere Admin |
| 7 | **Usuarios** | `DELETE` | `/usuarios/{id}` | Eliminar un usuario | Requiere Admin |
| 8 | **Estudiantes** | `POST` | `/estudiantes/` | Crear un nuevo perfil de estudiante | Requiere Token |
| 9 | **Estudiantes** | `GET` | `/estudiantes/` | Listar todos los estudiantes | Requiere Token |
| 10 | **Estudiantes** | `GET` | `/estudiantes/{id}` | Obtener estudiante por ID | Requiere Token |
| 11 | **Estudiantes** | `PUT` | `/estudiantes/{id}` | Actualizar estudiante | Requiere Admin / Instructor |
| 12 | **Estudiantes** | `DELETE` | `/estudiantes/{id}` | Eliminar estudiante | Requiere Admin |
| 13 | **Instructores** | `POST` | `/instructores/` | Crear un nuevo perfil de instructor | Requiere Admin |
| 14 | **Instructores** | `GET` | `/instructores/` | Listar todos los instructores | Requiere Token |
| 15 | **Instructores** | `GET` | `/instructores/{id}` | Obtener instructor por ID | Requiere Token |
| 16 | **Instructores** | `PUT` | `/instructores/{id}` | Actualizar instructor | Requiere Admin / Instructor |
| 17 | **Instructores** | `DELETE` | `/instructores/{id}` | Eliminar instructor | Requiere Admin |
| 18 | **Grupos** | `POST` | `/grupos/` | Crear un grupo de formación | Requiere Admin / Instructor |
| 19 | **Grupos** | `GET` | `/grupos/` | Listar todos los grupos | Requiere Token |
| 20 | **Grupos** | `GET` | `/grupos/{id}` | Obtener grupo por ID | Requiere Token |
| 21 | **Grupos** | `PUT` | `/grupos/{id}` | Actualizar información del grupo | Requiere Admin / Instructor |
| 22 | **Grupos** | `DELETE` | `/grupos/{id}` | Eliminar grupo | Requiere Admin |
| 23 | **Grupos** | `POST` | `/grupos/{id}/matricular` | Matricular un estudiante en un grupo | Requiere Admin / Instructor |
| 24 | **Trabajos** | `POST` | `/trabajos/` | Crear asignación/trabajo | Requiere Instructor |
| 25 | **Trabajos** | `GET` | `/trabajos/` | Listar todos los trabajos | Requiere Token |
| 26 | **Trabajos** | `GET` | `/trabajos/{id}` | Obtener trabajo por ID | Requiere Token |
| 27 | **Trabajos** | `PUT` | `/trabajos/{id}` | Actualizar trabajo | Requiere Instructor |
| 28 | **Trabajos** | `DELETE` | `/trabajos/{id}` | Eliminar trabajo | Requiere Instructor |
| 29 | **Entregas** | `POST` | `/entregas/` | Subir/crear entrega de evidencia | Requiere Token |
| 30 | **Entregas** | `GET` | `/entregas/` | Listar todas las entregas | Requiere Token |
| 31 | **Entregas** | `GET` | `/entregas/{id}` | Obtener entrega por ID | Requiere Token |
| 32 | **Entregas** | `PUT` | `/entregas/{id}` | Actualizar entrega | Requiere Token |
| 33 | **Entregas** | `DELETE` | `/entregas/{id}` | Eliminar entrega | Requiere Token |
| 34 | **Calificaciones** | `POST` | `/calificaciones/` | Evaluar y asignar calificación a entrega | Requiere Instructor |
| 35 | **Calificaciones** | `GET` | `/calificaciones/` | Listar todas las calificaciones | Requiere Token |
| 36 | **Calificaciones** | `GET` | `/calificaciones/{id}` | Obtener calificación por ID | Requiere Token |
| 37 | **Calificaciones** | `PUT` | `/calificaciones/{id}` | Actualizar calificación | Requiere Instructor |
| 38 | **Calificaciones** | `DELETE` | `/calificaciones/{id}` | Eliminar calificación | Requiere Instructor |
| 39 | **Asistencias** | `POST` | `/asistencias/` | Registrar asistencia | Requiere Instructor |
| 40 | **Asistencias** | `GET` | `/asistencias/` | Listar todos los registros de asistencia | Requiere Token |
| 41 | **Asistencias** | `GET` | `/asistencias/{id}` | Obtener asistencia por ID | Requiere Token |
| 42 | **Asistencias** | `PUT` | `/asistencias/{id}` | Actualizar estado de asistencia | Requiere Instructor |
| 43 | **Asistencias** | `DELETE` | `/asistencias/{id}` | Eliminar registro de asistencia | Requiere Instructor |
| 44 | **Notificaciones** | `POST` | `/notificaciones/` | Enviar una notificación | Requiere Admin / Instructor |
| 45 | **Notificaciones** | `GET` | `/notificaciones/` | Listar notificaciones | Requiere Token |
| 46 | **Notificaciones** | `GET` | `/notificaciones/mis-notificaciones` | Notificaciones del usuario actual | Requiere Token |
| 47 | **Notificaciones** | `PUT` | `/notificaciones/{id}/marcar-leida` | Marcar notificación como leída | Requiere Token |
| 48 | **Notificaciones** | `DELETE` | `/notificaciones/{id}` | Eliminar notificación | Requiere Token |

```

<FollowUp label="¿Quieres que preparemos los comandos Git para guardar todos los cambios?" query="Dame los comandos de Git para crear el commit con los 44 endpoints y el README.md actualizado."/>

```