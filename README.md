#README

## Descripción

Este proyecto es una aplicación de gestión de tareas que permite a los usuarios organizar y gestionar sus tareas diarias. Los usuarios pueden agregar, editar, eliminar y marcar tareas como completadas. La persistencia de los datos está garantizada mediante una base de datos SQLite.

# 📝 To-Do List App

Una aplicación de escritorio construida con Python y Tkinter para gestionar tareas personales, con inicio de sesión por usuario, almacenamiento en SQLite y una interfaz intuitiva.

---

## 📁 Estructura del Proyecto

El proyecto está organizado en una arquitectura por capas, separando interfaz gráfica, lógica de negocio, modelos y acceso a datos:

To-Do List/
│
├── database.db # Base de datos SQLite donde se almacenan usuarios y tareas
│
├── gui/ # Interfaces gráficas (pantallas)
│ ├── gui_dashboard.py # Pantalla principal con gestión de tareas
│ └── gui_login.py # Pantalla de inicio de sesión
│
├── models/ # Clases que representan las entidades del sistema
│ ├── tarea.py # Modelo de Tarea
│ └── usuario.py # Modelo de Usuario
│
├── repositories/ # Acceso directo a la base de datos (CRUD)
│ ├── tarea_repo.py # Operaciones sobre tareas en SQLite
│ └── usuario_repo.py # Operaciones sobre usuarios en SQLite
│
├── services/ # Lógica de negocio
│ ├── tarea_service.py # Gestión y validación de tareas
│ └── usuario_service.py # Registro, validación y autenticación de usuarios
│
├── main.py # Punto de entrada principal de la app
└── requirements.txt # Dependencias del proyecto


## Uso

### **Inicio de sesión**:
Al abrir la aplicación, se presentará una pantalla de login. Debes ingresar tu nombre de usuario y contraseña para acceder al sistema. Si las credenciales son correctas, serás redirigido a la pantalla principal donde podrás gestionar tus tareas.

### **Gestionar tareas**:
Después de iniciar sesión, podrás gestionar tus tareas desde el dashboard. Podrás:

- **Agregar nuevas tareas**: Puedes añadir nuevas tareas con un título, descripción, fecha de vencimiento, prioridad, y si la tarea es recurrente.
- **Editar tareas existentes**: Modificar cualquier campo de una tarea.
- **Eliminar tareas**: Eliminar tareas que ya no necesitas.
- **Marcar tareas como completadas**: Cambiar el estado de una tarea a "completada".

### **Ejemplo de creación de tarea**:
Para agregar una nueva tarea, puedes crear una instancia de la clase `Tarea` y luego agregarla utilizando el servicio correspondiente:

## 💡 Ejemplos

* **Crear un usuario** desde la interfaz de login:
  * Ingresa un nombre de usuario y contraseña únicos.
  * Se guarda automáticamente en la base de datos SQLite.

* **Agregar una tarea**:
  * Haz clic en “Agregar tarea”.
  * Completa título, descripción, prioridad, estado, fecha y si es recurrente.
  * Aparecerá en la lista de tareas asociadas a tu cuenta.

* **Estado de la tarea**:
  * Puedes cambiar el estado de "pendiente" a "completada" desde la interfaz.

```python
# Crear una nueva tarea
tarea = Tarea(
    titulo="Mi primera tarea",               # Título de la tarea
    descripcion="Descripción detallada de la tarea",  # Descripción de la tarea
    fecha_vencimiento="2025-12-31",           # Fecha de vencimiento
    estado="pendiente",                       # Estado de la tarea
    prioridad="media",                        # Prioridad (baja, media, alta)
    recurrente=0,                             # Si la tarea es recurrente (0: No, 1: Sí)
    frecuencia_recurrencia=None,              # Frecuencia de recurrencia (si es recurrente)
    id_usuario_creador=1                      # ID del usuario creador de la tarea
)

# Agregar la tarea utilizando el servicio de tareas
tarea_service.agregar_tarea(tarea)
