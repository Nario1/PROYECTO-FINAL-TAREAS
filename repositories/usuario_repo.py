from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.usuario import Usuario
from typing import Optional

class UsuarioRepo:
    """
    Repositorio ORM para manejar operaciones CRUD relacionadas con la entidad Usuario.
    Utiliza SQLAlchemy para interactuar con la base de datos.
    """

    def __init__(self, session: Session):
        self.session = session

    def crear_usuario(self, usuario: Usuario) -> Optional[Usuario]:
        try:
            self.session.add(usuario)
            self.session.commit()
            self.session.refresh(usuario)
            return usuario
        except IntegrityError:
            self.session.rollback()
            return None  # Usuario duplicado

    def obtener_por_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        return self.session.query(Usuario).filter_by(nombre_usuario=nombre_usuario).first()

    def validar_login(self, nombre_usuario: str, contraseña: str) -> bool:
        usuario = self.obtener_por_nombre(nombre_usuario)
        if usuario and usuario.contraseña == contraseña:
            return True
        return False
