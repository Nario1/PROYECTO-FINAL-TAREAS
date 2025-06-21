# models/usuario.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base  # ✅ Importar desde base.py, NO desde database

class Usuario(Base):
    """
    Modelo ORM que representa a un usuario en el sistema de gestión de tareas.
    """
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String, unique=True, nullable=False)
    contraseña = Column(String, nullable=False)

    # Relaciones
    tareas_creadas = relationship("Tarea", back_populates="creador")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre_usuario='{self.nombre_usuario}')>"
