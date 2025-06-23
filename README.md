
# 📝 To-Do List App

Una aplicación de escritorio construida con Python y Tkinter para gestionar tareas personales, con inicio de sesión por usuario, almacenamiento en SQLite y una interfaz intuitiva.

---

## 📌 Descripción

Este proyecto es una aplicación de gestión de tareas que permite a los usuarios organizar y gestionar sus tareas diarias. Los usuarios pueden agregar, editar, eliminar y marcar tareas como completadas. La persistencia de los datos está garantizada mediante una base de datos SQLite.

---

## 📁 Estructura del Proyecto

El proyecto está organizado en una arquitectura por capas, separando interfaz gráfica, lógica de negocio, modelos y acceso a datos:

```
To-Do List/
│
├── database.db                  # Base de datos SQLite
│
├── gui/                         # Interfaces gráficas (pantallas)
│   ├── gui_dashboard.py         # Pantalla principal
│   └── gui_login.py             # Pantalla de login
│
├── models/                      # Modelos de datos
│   ├── tarea.py                 # Modelo Tarea
│   └── usuario.py               # Modelo Usuario
│
├── repositories/                # Acceso a datos (repositorios)
│   ├── tarea_repo.py
│   └── usuario_repo.py
│
├── services/                    # Lógica de negocio
│   ├── tarea_service.py
│   └── usuario_service.py
│
├── utils/                       # Utilidades adicionales (notificaciones)
│   └── recordatorio_notificador.py
│
├── tests/                       # Pruebas unitarias y de aceptación
│   ├── conftest.py
│   ├── test_usuario.py
│   ├── test_tarea.py
│   ├── test_recordatorio.py
│   └── test_aceptacion.py
│
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

---

## 🚀 Uso de la Aplicación

### 🧑‍💻 Inicio de sesión
Al abrir la aplicación, se presentará una pantalla de login. Debes ingresar tu nombre de usuario y contraseña para acceder al sistema. Si las credenciales son correctas, serás redirigido al panel principal.

### ✅ Gestionar tareas
Una vez dentro del panel, podrás:

- 📝 Agregar nuevas tareas
- ✏️ Editar tareas existentes
- ❌ Eliminar tareas innecesarias
- ✔️ Marcar tareas como completadas
- 🔁 Crear tareas recurrentes
- 🔔 Configurar recordatorios

---

## 💡 Ejemplo de código

```python
# Crear una nueva tarea
tarea = Tarea(
    titulo="Mi primera tarea",
    descripcion="Descripción detallada de la tarea",
    fecha_vencimiento="2025-12-31",
    estado="pendiente",
    prioridad="media",
    recurrente=0,
    frecuencia_recurrencia=None,
    id_usuario_creador=1
)

# Agregar la tarea usando el servicio
tarea_service.agregar_tarea(tarea)
```

---

## 🧪 Pruebas Automatizadas

El proyecto incluye pruebas **unitarias** y **de aceptación**, ubicadas en la carpeta `tests/`.

### 📁 Estructura de pruebas:

```
tests/
├── conftest.py               # Configuración común de pruebas
├── test_usuario.py           # Registro y autenticación de usuarios
├── test_tarea.py             # Creación y listado de tareas
├── test_recordatorio.py      # Agregado y consulta de recordatorios
└── test_aceptacion.py        # Flujo completo desde login hasta recordatorio
```

### ✅ Ejecutar pruebas:

Desde la raíz del proyecto, ejecuta:

```bash
pytest tests/ -v
```

---

👨‍🎓 Autores
Nario Germán Reyes Ríos
Yohan Pool Ricse Peralta
John Espinoza Mendoza
Jose Samuel Delgadillo Pantoja
Henry Lozano Porta


Proyecto final para el curso Construccion de Software
Institución educativa – 2025

---

## 📄 Licencia

Este proyecto es de uso **educativo y personal**. Puedes adaptarlo libremente con fines no comerciales.
