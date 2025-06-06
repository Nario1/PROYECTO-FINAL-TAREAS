import sqlite3
from models.usuario import Usuario

class UsuarioRepo:
    def __init__(self, db_path):
        self.db_path = db_path
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT UNIQUE NOT NULL,
                    contraseña TEXT NOT NULL
                )
            ''')
            conn.commit()

    def crear_usuario(self, usuario: Usuario):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (?, ?)",
                (usuario.nombre_usuario, usuario.contraseña)
            )
            conn.commit()
            usuario.id = cursor.lastrowid
            return usuario

    def obtener_por_nombre(self, nombre_usuario):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre_usuario, contraseña FROM usuarios WHERE nombre_usuario = ?", (nombre_usuario,))
            row = cursor.fetchone()
            if row:
                return Usuario(id=row[0], nombre_usuario=row[1], contraseña=row[2])
            return None

    def validar_login(self, nombre_usuario, contraseña):
        usuario = self.obtener_por_nombre(nombre_usuario)
        if usuario and usuario.contraseña == contraseña:  # Aquí ideal comparar hash
            return True
        return False
