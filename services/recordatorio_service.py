from repositories.recordatorio_repo import RecordatorioRepo
from models.recordatorio import Recordatorio
from sqlalchemy.orm import Session
from typing import List, Optional

class RecordatorioService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = RecordatorioRepo(session)

    def agregar(self, rec: Recordatorio) -> Recordatorio:
        return self.repo.crear_recordatorio(rec)

    def editar(self, rec: Recordatorio) -> Recordatorio:
        return self.repo.actualizar_recordatorio(rec)

    def eliminar(self, id_rec: int) -> None:
        self.repo.eliminar_recordatorio(id_rec)

    def obtener_por_tarea(self, id_tarea: int) -> List[Recordatorio]:
        return self.repo.obtener_por_tarea(id_tarea)

    def obtener_por_usuario(self, id_usuario: int) -> List[Recordatorio]:
        """Devuelve todos los recordatorios de tareas cuyo usuario creador es el usuario indicado."""
        return (
            self.session.query(Recordatorio)
            .join(Recordatorio.tarea)
            .filter(Recordatorio.tarea.has(id_usuario_creador=id_usuario))
            .all()
        )

    def obtener_no_mostrados_por_usuario(self, id_usuario: int) -> List[Recordatorio]:
        """Devuelve los recordatorios no mostrados de tareas creadas por el usuario indicado."""
        return (
            self.session.query(Recordatorio)
            .join(Recordatorio.tarea)
            .filter(
                Recordatorio.mostrado.is_(False),
                Recordatorio.tarea.has(id_usuario_creador=id_usuario)
            )
            .all()
        )

    def obtener_por_id(self, id_rec: int) -> Optional[Recordatorio]:
        return self.repo.obtener_por_id(id_rec)

    def actualizar_recordatorio(self, recordatorio: Recordatorio):
        try:
            self.repo.actualizar_recordatorio(recordatorio)
        except Exception as e:
            print(f"Error al actualizar el recordatorio: {e}")
