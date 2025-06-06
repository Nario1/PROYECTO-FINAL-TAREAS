import tkinter as tk
from gui.gui_login import LoginGUI
from gui.gui_dashboard import DashboardGUI
from database import crear_bd_y_tablas

DB_PATH = "database.db"

def main():
    crear_bd_y_tablas(DB_PATH)

    root = tk.Tk()
    root.geometry("300x180")

    def on_login_success(nombre_usuario):
        root.withdraw()  # Ocultar ventana login
        dashboard_window = tk.Toplevel()
        dashboard_window.geometry("700x500")
        DashboardGUI(dashboard_window, DB_PATH, nombre_usuario)

    LoginGUI(root, DB_PATH, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
