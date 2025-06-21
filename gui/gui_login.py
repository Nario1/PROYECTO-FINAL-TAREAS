import tkinter as tk
from tkinter import messagebox
from services.usuario_service import UsuarioService
from database import SessionLocal

class LoginGUI:
    """Ventana de inicio de sesión con opción de registro."""

    def __init__(self, master, db_path, on_login_success):
        self.master = master
        self.master.title("Iniciar Sesión")
        self.session = SessionLocal()  # ✅ Se crea la sesión aquí
        self.usuario_service = UsuarioService(self.session)
        self.on_login_success = on_login_success  # Callback para abrir el dashboard si login es exitoso

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=20, pady=20)

        # Campo de usuario
        tk.Label(self.frame, text="Usuario:").grid(row=0, column=0, sticky="e")
        self.entry_usuario = tk.Entry(self.frame)
        self.entry_usuario.grid(row=0, column=1)

        # Campo de contraseña
        tk.Label(self.frame, text="Contraseña:").grid(row=1, column=0, sticky="e")
        self.entry_contraseña = tk.Entry(self.frame, show="*")
        self.entry_contraseña.grid(row=1, column=1)

        # Botón de login
        self.btn_login = tk.Button(self.frame, text="Iniciar Sesión", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=5)

        # Botón de registro
        self.btn_registrar = tk.Button(self.frame, text="Registrar", command=self.registrar)
        self.btn_registrar.grid(row=3, column=0, columnspan=2, pady=5)

    def login(self):
        """Valida el acceso del usuario."""
        usuario = self.entry_usuario.get().strip()
        contraseña = self.entry_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        if self.usuario_service.validar_login(usuario, contraseña):
            messagebox.showinfo("Éxito", f"Bienvenido, {usuario}.")
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def registrar(self):
        """Registra un nuevo usuario."""
        usuario = self.entry_usuario.get().strip()
        contraseña = self.entry_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        exito, mensaje = self.usuario_service.registrar_usuario(usuario, contraseña)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

__all__ = ['LoginGUI']
