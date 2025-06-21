from sqlalchemy.orm import Session
from repositories.usuario_repo import UsuarioRepo
from models.usuario import Usuario
from typing import Tuple


class UsuarioService:
    """
    Servicio que gestiona la lógica de negocio relacionada con usuarios.
    """

    def __init__(self, session: Session):
        """
        Inicializa el servicio con una sesión de SQLAlchemy.

        :param session: Sesión activa de SQLAlchemy.
        """
        self.usuario_repo = UsuarioRepo(session)

    def registrar_usuario(self, nombre_usuario: str, contraseña: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario si no existe previamente.

        :param nombre_usuario: Nombre del usuario.
        :param contraseña: Contraseña del usuario (sin hashear aún).
        :return: Tupla indicando si se registró correctamente y un mensaje.
        """
        usuario_existente = self.usuario_repo.obtener_por_nombre(nombre_usuario)
        if usuario_existente:
            return False, "El nombre de usuario ya existe."

        nuevo_usuario = Usuario(nombre_usuario=nombre_usuario, contraseña=contraseña)
        self.usuario_repo.crear_usuario(nuevo_usuario)
        return True, "Usuario registrado exitosamente."

    def validar_login(self, nombre_usuario: str, contraseña: str) -> bool:
        """
        Valida las credenciales del usuario.

        :param nombre_usuario: Nombre de usuario.
        :param contraseña: Contraseña proporcionada.
        :return: True si las credenciales son correctas, False en caso contrario.
        """
        return self.usuario_repo.validar_login(nombre_usuario, contraseña)
