from repositories.usuario_repo import UsuarioRepo
from models.usuario import Usuario

class UsuarioService:
    def __init__(self, db_path):
        self.usuario_repo = UsuarioRepo(db_path)

    def registrar_usuario(self, nombre_usuario, contraseña):
        usuario_existente = self.usuario_repo.obtener_por_nombre(nombre_usuario)
        if usuario_existente:
            return False, "El nombre de usuario ya existe."
        nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contraseña=contraseña)
        self.usuario_repo.crear_usuario(nuevo_usuario)
        return True, "Usuario registrado exitosamente."

    def validar_login(self, nombre_usuario, contraseña):
        return self.usuario_repo.validar_login(nombre_usuario, contraseña)
