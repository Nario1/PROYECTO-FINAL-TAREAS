from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_vencimiento = Column(Date)
    estado = Column(String, default='pendiente')
    prioridad = Column(String, default='media')
    recurrente = Column(Integer, default=0)
    frecuencia_recurrencia = Column(String)
    id_usuario_creador = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    creador = relationship("Usuario", back_populates="tareas_creadas")

    # Relación uno-a-muchos con recordatorios
    recordatorios = relationship("Recordatorio", back_populates="tarea", cascade="all, delete-orphan")

    def __init__(self, titulo, descripcion=None, fecha_vencimiento=None, estado='pendiente',
                 prioridad='media', recurrente=0, frecuencia_recurrencia=None, id_usuario_creador=None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.prioridad = prioridad
        self.recurrente = recurrente
        self.frecuencia_recurrencia = frecuencia_recurrencia
        self.id_usuario_creador = id_usuario_creador

    def __repr__(self):
        return f"<Tarea(id={self.id}, titulo='{self.titulo}', estado='{self.estado}')>"
