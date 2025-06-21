from sqlalchemy.orm import Session
from models.tarea import Tarea
from typing import List, Optional

class TareaRepo:
    """
    Repositorio ORM para manejar operaciones CRUD relacionadas con la entidad Tarea.
    Utiliza SQLAlchemy y sesiones para interactuar con la base de datos.
    """

    def __init__(self, session: Session):
        self.session = session

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        self.session.add(tarea)
        self.session.commit()
        self.session.refresh(tarea)
        return tarea

    def actualizar_tarea(self, tarea: Tarea) -> None:
        self.session.merge(tarea)
        self.session.commit()

    def eliminar_tarea(self, id_tarea: int) -> None:
        tarea = self.session.get(Tarea, id_tarea)
        if tarea:
            self.session.delete(tarea)
            self.session.commit()

    def obtener_tareas_por_usuario(self, id_usuario: int) -> List[Tarea]:
        return self.session.query(Tarea).filter_by(id_usuario_creador=id_usuario).all()

    def buscar_tarea_por_titulo(self, id_usuario: int, titulo: str) -> List[Tarea]:
        return self.session.query(Tarea).filter(
            Tarea.id_usuario_creador == id_usuario,
            Tarea.titulo.ilike(f'%{titulo}%')
        ).all()

    def marcar_completada(self, id_tarea: int) -> None:
        tarea = self.session.get(Tarea, id_tarea)
        if tarea:
            tarea.estado = "completada"
            self.session.commit()
