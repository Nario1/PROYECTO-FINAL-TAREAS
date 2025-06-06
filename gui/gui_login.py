import tkinter as tk
from tkinter import messagebox
from services.usuario_service import UsuarioService

class LoginGUI:
    def __init__(self, master, db_path, on_login_success):
        self.master = master
        self.master.title("Login")
        self.usuario_service = UsuarioService(db_path)
        self.on_login_success = on_login_success

        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        tk.Label(self.frame, text="Usuario:").grid(row=0, column=0, sticky="e")
        self.entry_usuario = tk.Entry(self.frame)
        self.entry_usuario.grid(row=0, column=1)

        tk.Label(self.frame, text="Contraseña:").grid(row=1, column=0, sticky="e")
        self.entry_contraseña = tk.Entry(self.frame, show="*")
        self.entry_contraseña.grid(row=1, column=1)

        self.btn_login = tk.Button(self.frame, text="Iniciar Sesión", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=5)

        self.btn_registrar = tk.Button(self.frame, text="Registrar", command=self.registrar)
        self.btn_registrar.grid(row=3, column=0, columnspan=2, pady=5)

    def login(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        if self.usuario_service.validar_login(usuario, contraseña):
            messagebox.showinfo("Éxito", "Login correcto")
            self.on_login_success(usuario)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def registrar(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        exito, mensaje = self.usuario_service.registrar_usuario(usuario, contraseña)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)
