

```markdown
# 🚀 API de Gestión de Grupos, Trabajos y Entregas

API RESTful construida con **FastAPI**, **SQLAlchemy** y **SQLite** (o PostgreSQL) para la administración de entornos educativos. Permite gestionar usuarios (Instructores y Estudiantes), la creación de grupos, la asignación de trabajos y la recepción de entregas individuales.

---

## 📋 Tabla de Contenidos

- [Características Principal](#-características-principales)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Modelo de Base de Datos (Relaciones)](#-modelo-de-base-de-datos-relaciones)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Ejecución del Servidor](#-ejecución-del-servidor)
- [Documentación Interactiva (Endpoints)](#-documentación-interactiva-endpoints)

---

## ✨ Características Principales

1. **Gestión de Usuarios**: Registro e inicio de sesión con roles diferenciados (`instructor` y `estudiante`).
2. **Gestión de Grupos**: Los instructores pueden crear grupos con un código único de acceso.
3. **Asignación de Trabajos**: Asignación de tareas con títulos, descripciones y fechas límite vinculadas a un grupo específico.
4. **Entregas Individuales**: Los estudiantes pueden enviar sus actividades o trabajos asignados, registrando el enlace o archivo entregable y el estado de revisión (`entregado`, `aprobado`, `reprobado`).

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.10+
- **Framework Web**: FastAPI
- **Servidor ASGI**: Uvicorn
- **ORM**: SQLAlchemy
- **Validación de Datos**: Pydantic v2
- **Base de Datos**: SQLite (por defecto en desarrollo)

---

## 📂 Estructura del Proyecto

```text
api_gestion_grupos/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de FastAPI
│   ├── database.py          # Configuración de SQLAlchemy y motor DB
│   ├── models/              # Modelos de SQLAlchemy
│   │   ├── __init__.py      # Exportación centralizada de modelos
│   │   ├── usuario.py
│   │   ├── grupo.py
│   │   ├── trabajo.py
│   │   └── entrega.py
│   ├── schemas/             # Modelos y esquemas de Pydantic
│   │   └── ...
│   └── routers/             # Endpoints y rutas divididos por módulos
│       ├── usuarios.py
│       ├── grupos.py
│       ├── trabajos.py
│       ├── entregas.py
│       └── auth.py
├── venv/                    # Entorno virtual
├── requirements.txt         # Dependencias del proyecto
└── README.md

```

---

## 🗄️ Modelo de Base de Datos (Relaciones)

El sistema utiliza una arquitectura relacional bidireccional mediante `relationship` y `back_populates` en SQLAlchemy:

```
[ Usuario ] (1) <--- crea ---> (N) [ Grupo ]
    |                                 |
 (recibe)                          (asigna)
    |                                 |
    v                                 v
[ Entrega ] (N) <--- entrega --- (1) [ Trabajo ]

```

### Detalle de Entidades:

1. **`Usuario` (`usuarios`)**
* `id`: Integer (PK, Index)
* `nombre`: String
* `correo`: String (Unique, Index)
* `password`: String
* `rol`: String (`instructor` | `estudiante`)
* *Relaciones*: `grupos_creados` (1:N hacia Grupo), `entregas` (1:N hacia Entrega).


2. **`Grupo` (`grupos`)**
* `id`: Integer (PK, Index)
* `nombre`: String
* `codigo`: String (Unique, Index)
* `instructor_id`: Integer (FK -> `usuarios.id`)
* *Relaciones*: `instructor` (N:1 hacia Usuario), `trabajos` (1:N hacia Trabajo con `cascade="all, delete-orphan"`).


3. **`Trabajo` (`trabajos`)**
* `id`: Integer (PK, Index)
* `grupo_id`: Integer (FK -> `grupos.id`)
* `titulo`: String
* `descripcion`: String (Nullable)
* `fecha_limite`: DateTime (Nullable)
* *Relaciones*: `grupo` (N:1 hacia Grupo), `entregas` (1:N hacia Entrega con `cascade="all, delete-orphan"`).


4. **`Entrega` (`entregas`)**
* `id`: Integer (PK, Index)
* `trabajo_id`: Integer (FK -> `trabajos.id`)
* `estudiante_id`: Integer (FK -> `usuarios.id`)
* `entregable`: String (URL o texto del entregable)
* `estado`: String (Default: `"entregado"`)
* `fecha_entrega`: DateTime (Default: `utcnow`)
* *Relaciones*: `trabajo` (N:1 hacia Trabajo), `estudiante` (N:1 hacia Usuario).



---

## ⚡ Instalación y Configuración

### 1. Clonar el repositorio y entrar al proyecto

```bash
git clone <https://github.com/chalarca14/Api_Gestio_Grupos.git>
cd api_gestion_grupos

```

### 2. Crear y activar el entorno virtual

* **Windows**:
```powershell
python -m venv venv
.\venv\Scripts\activate

```


* **Linux / macOS**:
```bash
python3 -m venv venv
source venv/bin/activate

```



### 3. Instalar dependencias

```bash
pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose

```

---

## 🚀 Ejecución del Servidor

Inicia el servidor de desarrollo en modo de recarga automática (`--reload`):

```bash
uvicorn app.main:app --reload

```

Si todo está configurado correctamente, verás en consola:

```text
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)

```

---

## 📖 Documentación Interactiva (Endpoints)

FastAPI genera documentación automática interactiva para probar los endpoints directamente desde el navegador:

* **Swagger UI**: [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)

### Principales Rutas Disponibles:

| Módulo | Método | Ruta | Descripción |
| --- | --- | --- | --- |
| **Auth** | `POST` | `/auth/login` | Autenticación y generación de Token / Sesión |
| **Usuarios** | `POST` | `/usuarios/` | Registrar un nuevo usuario |
|  | `GET` | `/usuarios/` | Listar todos los usuarios |
| **Grupos** | `POST` | `/grupos/` | Crear un grupo (requiere rol Instructor) |
|  | `GET` | `/grupos/` | Listar los grupos disponibles |
| **Trabajos** | `POST` | `/trabajos/` | Crear una asignación/trabajo dentro de un grupo |
|  | `GET` | `/trabajos/` | Obtener tareas y sus especificaciones |
| **Entregas** | `POST` | `/entregas/` | Subir una entrega vinculada a un estudiante y trabajo |
|  | `GET` | `/entregas/` | Consultar las entregas realizadas |

---

## 💡 Solución de Problemas Frecuentes

Si realizas cambios en la estructura de los modelos SQLAlchemy y obtienes errores de integridad o `KeyError` al iniciar o consultar la API:

1. Detén el servidor con `CTRL + C`.
2. Si utilizas SQLite, elimina el archivo local de la base de datos (por ejemplo, `gestion_grupos.db`).
3. Vuelve a iniciar el servidor con `uvicorn app.main:app --reload` para recrear las tablas con la estructura limpia.

```

<ElicitationsGroup message="Para completar el despliegue o la documentación de la API:">
  <Elicitation label="Generar archivo requirements.txt completo" query="Genera el contenido del archivo requirements.txt para congelar las versiones de las librerías del proyecto."/>
  <Elicitation label="Escribir colección de pruebas con Postman" query="¿Cómo exportar o estructurar los endpoints de esta API para realizar pruebas en Postman?"/>
</ElicitationsGroup>

```