from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id = Column(Integer, primary_key=True)
    mensaje = Column(String, nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    id_tarea = Column(Integer, ForeignKey("tareas.id"), nullable=False)
    mostrado = Column(Boolean, default=False)

    tarea = relationship("Tarea", back_populates="recordatorios")

    def __init__(self, mensaje, fecha_hora, id_tarea):
        self.mensaje = mensaje
        self.fecha_hora = fecha_hora
        self.id_tarea = id_tarea

    def __repr__(self):
        return f"<Recordatorio(id={self.id}, mensaje='{self.mensaje}', fecha_hora={self.fecha_hora})>"
