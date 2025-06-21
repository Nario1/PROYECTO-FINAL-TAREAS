import tkinter as tk
from gui.gui_login import LoginGUI
from gui.gui_dashboard import DashboardGUI
from database import crear_bd_y_tablas

DB_PATH = "database.db"  # Ruta de la base de datos, útil si la pasas a otros módulos

def main():
    """
    Punto de entrada principal del programa.
    - Crea la base de datos y sus tablas si no existen.
    - Inicia la interfaz de login con Tkinter.
    """

    # Inicializar la base de datos (SQLAlchemy)
    crear_bd_y_tablas()  # No se pasa ruta, ya está configurado en `database.py`

    # Crear la ventana principal de la app (Login)
    root = tk.Tk()
    root.title("Gestor de Tareas")
    root.geometry("300x180")
    root.resizable(False, False)

    def on_login_success(nombre_usuario: str) -> None:
        """
        Función que se ejecuta al iniciar sesión correctamente.
        Oculta la ventana de login y muestra el panel de tareas.

        :param nombre_usuario: Nombre del usuario autenticado.
        """
        root.withdraw()  # Ocultar la ventana de login
        dashboard_window = tk.Toplevel()
        dashboard_window.title("Panel de Tareas")
        dashboard_window.geometry("700x500")
        dashboard_window.resizable(True, True)
        DashboardGUI(dashboard_window, DB_PATH, nombre_usuario)

    # Mostrar la interfaz de login
    LoginGUI(root, DB_PATH, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
